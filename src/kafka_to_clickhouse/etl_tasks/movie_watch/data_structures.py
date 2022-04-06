import datetime
import uuid
from dataclasses import astuple, dataclass

from confluent_kafka import Message
from orjson import orjson

from etl_tasks.abc_data_structure import TransferClass


@dataclass(frozen=True)
class MovieWatch(TransferClass):
    __slots__ = ('movie_id', 'client_id', 'view_date', 'view_ts')
    movie_id: uuid.UUID
    client_id: uuid.UUID
    view_date: datetime.date
    view_ts: int

    @staticmethod
    def create_from_message(message: Message) -> 'MovieWatch':
        record: dict = orjson.loads(message.value())
        _, view_date_ms = message.timestamp()
        view_date_ts = view_date_ms / 1000.0
        return MovieWatch(
            movie_id=uuid.UUID(record['movie_id']),
            client_id=uuid.UUID(record['client_id']),
            view_date=datetime.datetime.utcfromtimestamp(view_date_ts).date(),
            view_ts=record.get('view_ts', 0),
        )

    @staticmethod
    def get_insert_query() -> str:
        return """INSERT INTO movie_watches (MovieID, UserID, ViewDate, ViewTimestamp) VALUES"""

    def get_tuple(self) -> tuple:
        return astuple(self)
