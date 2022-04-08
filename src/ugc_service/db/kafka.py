import logging
from typing import Optional

import backoff
from aiokafka import AIOKafkaProducer
from core.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_REQUEST_TIMEOUT_MS
from core.utils import backoff_hdlr
from kafka.errors import KafkaConnectionError

logger = logging.getLogger(__name__)
kafka_producer: Optional[AIOKafkaProducer] = None


async def get_kafka_producer() -> AIOKafkaProducer:
    """Возвращает объект для асинхронного общения с сервисами Apache Kafka.
    Функция понадобится при внедрении зависимостей."""
    return kafka_producer


@backoff.on_exception(backoff.expo, KafkaConnectionError, on_backoff=backoff_hdlr)
async def kafka_reconnect():
    """Устанавливает подключение к сервису Apache Kafka."""
    global kafka_producer
    if kafka_producer:
        await kafka_producer.stop()
        await kafka_producer.client.close()
    logger.info('Check connection to Kafka server.')
    kafka_producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        request_timeout_ms=KAFKA_REQUEST_TIMEOUT_MS,
    )
    await kafka_producer.start()
    logger.info('Successfully connected to Kafka server.')


async def kafka_disconnect():
    """Закрывает подключение к сервису Apache Kafka."""
    global kafka_producer
    await kafka_producer.stop()
    logger.info(' Successfully disconnected from Kafka server.')
