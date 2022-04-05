from clickhouse_driver import Client

from settings.settings import ClickHouseSettings


def get_client(settings: ClickHouseSettings) -> Client:
    client = Client(**settings.dict())
    return client
