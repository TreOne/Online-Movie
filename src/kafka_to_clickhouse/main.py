from typing import Type

from clickhouse_driver import Client
from confluent_kafka import Consumer

from engines.click_house import get_client
from engines.kafka import get_consumer
from etl_tasks.abc_data_structure import TransferClass
from settings.settings import Settings


def main():
    settings = Settings()
    clickhouse: Client = get_client(settings.clickhouse)
    kafka: Consumer = get_consumer(settings.kafka)

    for task in settings.tasks:
        print(f'Starting the task "{task.task_name}"')
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
            clickhouse.execute(query, data)

        kafka.unsubscribe()

    kafka.close()
    clickhouse.disconnect()


if __name__ == '__main__':
    main()
