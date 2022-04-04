from clickhouse_driver import Client


def get_client():
    client = Client(host='clickhouse')
    return client
