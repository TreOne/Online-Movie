from typing import Generator, Optional

from clickhouse_driver import Client
from clickhouse_driver.errors import ServerException
from confluent_kafka import Consumer, Message
from utils import get_logger

logger = get_logger('main')


def loader(
        clickhouse: Client, kafka_consumer: Consumer, query: str,
        task_data: Generator, last_kafka_message: Optional[Message],
) -> None:
    """
    Load transformed Kafka messages in ClickHouse and commit it

    @param clickhouse: ClickHouse instance
    @param kafka_consumer: Kafka Consumer instance
    @param query: Load Query for ClickHouse
    @param task_data: transformed data for loading
    @param last_kafka_message: Last message from Kafka for offset committing
    @return: None
    """
    if last_kafka_message:
        try:
            number_inserted_rows: int = clickhouse.execute(query=query, params=task_data)
            logger.info(
                f'Successfully added {number_inserted_rows} new messages to ClickHouse',
            )
        except ServerException as e:
            logger.exception(f'ClickHouse error: {e}')
        kafka_consumer.commit(last_kafka_message)
        logger.info(f'Set offset to {last_kafka_message.offset()}.')
    else:
        logger.debug('No new messages.')
