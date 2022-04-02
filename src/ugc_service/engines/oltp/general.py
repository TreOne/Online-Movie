from abc import ABC, abstractmethod


class OLTPEngine(ABC):
    """
    Абстрактный класс OLTP-системы.
    """

    @abstractmethod
    async def send(self, topic: str, message: bytes) -> None:
        """Посылает сообщение в OLTP систему."""
        pass
