from http import HTTPStatus

from aiokafka import AIOKafkaProducer
from db.kafka import kafka_reconnect
from engines.oltp.general import OLTPEngine
from fastapi import HTTPException
from kafka.errors import KafkaError


class KafkaOLTPEngine(OLTPEngine):
    """
    Реализация OLTP-системы на основе Apache Kafka.
    """

    def __init__(self, kafka_producer: AIOKafkaProducer):
        self.kafka_producer = kafka_producer

    async def send(self, topic: str, message: bytes) -> None:
        try:
            await self.kafka_producer.send_and_wait(topic=topic, value=message)
        except KafkaError:
            await kafka_reconnect()
            raise HTTPException(
                status_code=HTTPStatus.GATEWAY_TIMEOUT,
                detail='The database is not responding.',
            )
