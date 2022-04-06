from typing import Type

from clickhouse_driver import Client
from clickhouse_driver.errors import ServerException
from confluent_kafka import Consumer

from engines.click_house import create_table, get_client, table_is_exist
from engines.kafka import get_consumer
from etl_tasks.abc_data_structure import TransferClass
from settings.settings import Settings

from apscheduler.schedulers.blocking import BlockingScheduler

my_scheduler = BlockingScheduler()


@my_scheduler.scheduled_job('interval', hours=1)
def etl_process():
    settings = Settings()
    clickhouse: Client = get_client(settings.clickhouse)
    kafka: Consumer = get_consumer(settings.kafka)

    for task in settings.tasks:
        print(f'Starting the task "{task.task_name}"')
        if not table_is_exist(clickhouse, task.clickhouse.table):
            create_table(clickhouse, task.clickhouse.table_ddl.read_text('utf-8'))
        kafka.subscribe(topics=task.kafka.topics)

        messages = kafka.consume(num_messages=task.num_messages, timeout=task.kafka.timeout)
        data_class: Type[TransferClass] = task.data_class
        watches = []
        for message in messages:
            if not message:
                break
            watch = data_class.create_from_message(message)
            watches.append(watch)
        del messages

        if watches:
            print(f'Messages received: {len(watches)}')
            data = [watch.get_tuple() for watch in watches]
            query = data_class.get_insert_query()
            try:
                result = clickhouse.execute(query, data)
            except ServerException as e:
                # TODO: КХ ответил ошибкой. Что делаем? Пробуем еще раз или откатываем сдвиг полученных сообщений?
                print(f'ClickHouse Error: {e}')
        else:
            print('No new messages.')

        kafka.unsubscribe()

    kafka.close()
    clickhouse.disconnect()


if __name__ == '__main__':
    my_scheduler.start()
