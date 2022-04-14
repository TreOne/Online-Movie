from typing import List

from clickhouse_driver import Client
from utils import get_logger

logger = get_logger(__name__)


def loader(clickhouse: Client, query: str, task_data: List[tuple]) -> None:
    """Load transformed Kafka messages in ClickHouse"""
    number_inserted_rows: int = clickhouse.execute(query=query, params=task_data)
    logger.info(f'Add {number_inserted_rows} new messages to ClickHouse.')
