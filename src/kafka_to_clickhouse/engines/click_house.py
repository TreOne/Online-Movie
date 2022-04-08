from clickhouse_driver import Client
from settings.settings import ClickHouseSettings


def get_client(settings: ClickHouseSettings) -> Client:
    client = Client(**settings.dict())
    return client


def table_is_exist(client: Client, table_name: str) -> bool:
    query = f'EXISTS TABLE {table_name}'
    result = bool(client.execute(query)[0][0])  # Возвращается список кортежей. [(0,)] или [(1,)]
    return result


def create_table(client: Client, ddl: str):
    client.execute(ddl)
