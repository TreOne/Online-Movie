import gc
import time
from typing import Generator, List, Optional, Tuple

from clickhouse_driver import Client
from confluent_kafka import Consumer, Message
from engines.click_house import get_client
from settings.settings import Settings
from utils import extractor, get_kafka_tasks, get_logger, loader, transformer

logger = get_logger('main')


def etl_process() -> None:
    """
    Infinity ETL process for data migration from Kafka to ClickHouse

    @return: None
    """
    logger.info('Initializing the application...')
    settings = Settings()
    clickhouse: Client = get_client(settings.clickhouse)
    kafka_consumers: List[Tuple] = get_kafka_tasks(
        settings=settings, clickhouse=clickhouse,
    )
    logger.info('Starting an infinite ETL loop...')
    while True:
        for kafka_consumer, data_class, num_messages in kafka_consumers:
            # Extract data from Kafka
            kafka_messages: List[Message] = extractor(
                kafka_consumer=kafka_consumer, num_messages=num_messages,
            )
            # Transform data from Kafka
            task_data: Generator = transformer(
                data_class=data_class, kafka_messages=kafka_messages,
            )
            # get last message from Kafka
            last_kafka_message: Optional[Message] = (
                kafka_messages[-1] if kafka_messages else None
            )
            # clear kafka_messages list
            kafka_messages.clear()
            # Load data in ClickHouse
            loader(
                clickhouse=clickhouse,
                kafka_consumer=kafka_consumer,
                query=data_class.get_insert_query(),
                task_data=task_data,
                last_kafka_message=last_kafka_message,
            )
            # call garbage collector
            gc.collect()

        logger.debug(f'The cycle is over, we fall asleep for {settings.cycles_delay} seconds.')
        time.sleep(settings.cycles_delay)


if __name__ == '__main__':
    etl_process()
