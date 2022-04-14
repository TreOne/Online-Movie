from typing import List, Tuple, Type

from clickhouse_driver import Client
from confluent_kafka import Consumer, Message
from engines.click_house import create_table, table_is_exist
from engines.kafka import get_consumer
from etl_tasks.abc_data_structure import TransferClass
from settings.settings import ClickHouseTaskSettings, Settings
from utils import get_logger

logger = get_logger(__name__)


def check_clickhouse_table(
        clickhouse: Client, clickhouse_task_settings: ClickHouseTaskSettings,
) -> None:
    """
    This method check that table exists in Clickhouse else create it

    @param clickhouse: ClickHouse instance
    @param clickhouse_task_settings: Task's settings for Clickhouse table
    @return: None
    """
    clickhouse_table: str = clickhouse_task_settings.table
    logger.info(f'Check ClickHouse table "{clickhouse_table}"')
    if not table_is_exist(
            client=clickhouse, table_name=clickhouse_table,
    ):
        logger.info(f'Creating a table "{clickhouse_table}".')
        create_table(
            client=clickhouse,
            ddl=clickhouse_task_settings.table_ddl.read_text('utf-8'),
        )


def get_kafka_tasks(settings: Settings, clickhouse: Client) -> List[Tuple]:
    """
    This method determine Transfer class for each task and
    create Kafka consumers, which already subscribed for specific topics

    @param settings:
    @param clickhouse: Storage for OLAP system
    @return: List with tuples, which include
             Kafka's Consumer, Transfer Class & number for batch load
    """
    kafka_task_data: List[Tuple] = []
    for task in settings.tasks:
        check_clickhouse_table(
            clickhouse=clickhouse,
            clickhouse_task_settings=task.clickhouse,
        )
        logger.info(f'Init Kafka consumer for task "{task.task_name}"')
        kafka_task_consumer: Consumer = get_consumer(task.kafka)
        data_class: Type[TransferClass] = task.data_class
        num_messages: int = task.num_messages

        logger.debug(f'"{task.task_name}" subscribes for topics: {task.kafka.topics}')
        kafka_task_consumer.subscribe(topics=task.kafka.topics)
        # Add task data in result List
        kafka_task_data.append(
            tuple([kafka_task_consumer, data_class, num_messages]),
        )
    return kafka_task_data
