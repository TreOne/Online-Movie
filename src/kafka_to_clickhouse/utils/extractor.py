from typing import List

from confluent_kafka import Consumer, Message
from utils import get_logger

logger = get_logger('main')


def extractor(kafka_consumer: Consumer, num_messages: int) -> List[Message]:
    """
    Method get data from specific Kafka's topic(s)

    @param kafka_consumer: Kafka Consumer instance
    @param num_messages: count of messages which need to get
    @return: List of messages from Kafka storage
    """
    logger.debug(f'Trying to consume {num_messages} messages.')
    kafka_messages: List[Message] = kafka_consumer.consume(
        num_messages=num_messages, timeout=1.0,
    )
    logger.debug(f'Received messages: {len(kafka_messages)}')
    return kafka_messages
