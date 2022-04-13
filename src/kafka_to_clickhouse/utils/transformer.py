from typing import Generator, List, Type

from confluent_kafka import Consumer, Message
from etl_tasks.abc_data_structure import TransferClass
from utils import get_logger

logger = get_logger('main')


def transformer(
        data_class: Type[TransferClass], kafka_messages: List[Message],
) -> Generator:
    """
    Transform kafka messages in specific format
    before to send them in ClickHouse

    @param data_class: Class for data transforming
    @param kafka_messages: messages from Kafka for ETL process
    @return: Generator with kafka messages
    """
    logger.info(f'Transformed kafka data: {len(kafka_messages)} messages')
    return (
        data_class.create_from_message(kafka_message).get_tuple()
        for kafka_message in kafka_messages
    )
