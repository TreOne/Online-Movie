from functools import lru_cache
from uuid import UUID

from aiokafka import AIOKafkaProducer
from db.kafka import get_kafka_producer
from engines.oltp.general import OLTPEngine
from engines.oltp.kafka import KafkaOLTPEngine
from fastapi import Depends


class WatcherService:
    def __init__(self, oltp_engine: OLTPEngine):
        self.oltp_engine = oltp_engine

    async def register_movie_watch(
        self, movie_id: UUID, client_id: UUID, view_ts: int
    ) -> None:
        """Регистрирует сообщение о прогрессе просмотра фильма."""
        message = f"movie_id={movie_id}|client_id={client_id}|view_ts={view_ts}"
        await self.oltp_engine.send(topic="movie_watches", message=message.encode())


@lru_cache()
def get_watcher_service(
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> WatcherService:
    kafka_oltp = KafkaOLTPEngine(kafka_producer)
    return WatcherService(oltp_engine=kafka_oltp)
