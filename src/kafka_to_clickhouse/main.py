import gc
import time
from typing import List, Type

from clickhouse_driver import Client
from clickhouse_driver.errors import ServerException
from confluent_kafka import Consumer, Message

from engines.click_house import create_table, get_client, table_is_exist
from engines.kafka import get_consumer
from etl_tasks.abc_data_structure import TransferClass
from settings.settings import Settings
from utils import get_logger

logger = get_logger('main')


def etl_process():
    logger.info('Initializing the application...')
    settings = Settings()
    clickhouse: Client = get_client(settings.clickhouse)
    kafka: Consumer = get_consumer(settings.kafka)

    logger.info('Starting an infinite ETL loop...')
    while True:
        for task in settings.tasks:
            logger.info(f'Starting the task "{task.task_name}"')
            if not table_is_exist(clickhouse, task.clickhouse.table):
                logger.info(f'Creating a table "{task.clickhouse.table}".')
                create_table(clickhouse, task.clickhouse.table_ddl.read_text('utf-8'))
            logger.debug(f'Subscribes for topics: {task.kafka.topics}')
            kafka.subscribe(topics=task.kafka.topics)

            logger.debug(f'Trying to consume {task.num_messages} messages.')
            kafka_messages: List = kafka.consume(num_messages=task.num_messages, timeout=1.0)
            logger.debug(f'Received messages: {len(kafka_messages)}')
            data_class: Type[TransferClass] = task.data_class
            task_data = []
            for kafka_message in kafka_messages:
                item = data_class.create_from_message(kafka_message)
                task_data.append(item)
            last_kafka_message: Message = kafka_messages[-1] if kafka_messages else None
            kafka_messages.clear()

            if task_data:
                query_tuples = [item.get_tuple() for item in task_data]
                query = data_class.get_insert_query()
                try:
                    clickhouse.execute(query, query_tuples)
                    logger.info(f'Set offset to {last_kafka_message.offset()}.')
                    kafka.commit(last_kafka_message)
                    logger.info(f'Successfully added {len(query_tuples)} new messages to ClickHouse')
                except ServerException as e:
                    logger.exception(f'ClickHouse error: {e}')
            else:
                logger.debug('No new messages.')

            gc.collect()
            kafka.unsubscribe()

        logger.debug(f'The cycle is over, we fall asleep for {settings.cycles_delay} seconds.')
        time.sleep(settings.cycles_delay)


if __name__ == '__main__':
    etl_process()
