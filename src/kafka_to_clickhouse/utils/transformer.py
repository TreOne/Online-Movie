from typing import List, Tuple, Type

from confluent_kafka import Message
from etl_tasks.abc_data_structure import TransferClass
from utils import get_logger

logger = get_logger(__name__)


def transformer(
        data_class: Type[TransferClass], kafka_messages: List[Message],
) -> List[Tuple]:
    """Transform kafka messages in specific format."""
    logger.info(f'Transformed kafka data: {len(kafka_messages)} messages')
    return [
        data_class.create_from_message(kafka_message).get_tuple()
        for kafka_message in kafka_messages
    ]
