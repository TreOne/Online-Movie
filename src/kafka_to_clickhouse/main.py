import gc
import time
from typing import List, Tuple

from clickhouse_driver import Client
from clickhouse_driver.errors import ServerException
from confluent_kafka import Message
from engines.click_house import get_client
from settings.settings import Settings
from utils import extractor, get_kafka_tasks, get_logger, loader, transformer

logger = get_logger('main')


def etl_process() -> None:
    """Infinity ETL process for data migration from Kafka to ClickHouse."""
    logger.info('Initializing the application...')
    settings = Settings()
    clickhouse: Client = get_client(settings.clickhouse)
    kafka_consumers: List[Tuple] = get_kafka_tasks(
        settings=settings, clickhouse=clickhouse,
    )
    logger.info('Starting an infinite ETL loop...')
    while True:
        for kafka_consumer, data_class, num_messages in kafka_consumers:
            kafka_messages: List[Message] = extractor(
                kafka_consumer=kafka_consumer, num_messages=num_messages,
            )

            task_data: List[tuple] = transformer(
                data_class=data_class, kafka_messages=kafka_messages,
            )

            if kafka_messages:
                last_kafka_message = kafka_messages[-1]
                try:
                    loader(
                        clickhouse=clickhouse,
                        query=data_class.get_insert_query(),
                        task_data=task_data,
                    )
                except ServerException as e:
                    logger.exception(f'ClickHouse error: {e}')
                else:
                    kafka_consumer.commit(last_kafka_message)
                    logger.info(f'Set offset to {last_kafka_message.offset()}.')
            else:
                logger.debug('No new messages.')

            kafka_messages.clear()
            gc.collect()

        logger.debug(f'The cycle is over, we fall asleep for {settings.cycles_delay} seconds.')
        time.sleep(settings.cycles_delay)


if __name__ == '__main__':
    etl_process()
