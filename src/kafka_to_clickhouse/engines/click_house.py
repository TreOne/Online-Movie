from clickhouse_driver import Client
from settings.settings import ClickHouseSettings


def get_client(settings: ClickHouseSettings) -> Client:
    client = Client(**settings.dict())
    return client


def table_is_exist(client: Client, table_name: str) -> bool:
    query: str = f'EXISTS TABLE {table_name}'
    # Возвращается список кортежей. [(0,)] или [(1,)]
    result: bool = bool(client.execute(query)[0][0])
    return result


def create_table(client: Client, ddl: str) -> None:
    client.execute(ddl)
