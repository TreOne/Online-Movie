from abc import ABC, abstractmethod

from confluent_kafka import Message


class TransferClass(ABC):

    @staticmethod
    @abstractmethod
    def create_from_message(message: Message) -> 'TransferClass':
        pass

    @staticmethod
    @abstractmethod
    def get_insert_query() -> str:
        pass

    @abstractmethod
    def get_tuple(self) -> tuple:
        pass
