import datetime
import random
import time
import uuid
from typing import List

import psycopg2
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from clickhouse_driver import Client
from psycopg2.extras import execute_values

CHUNK_SIZE = 100_000

# MESSAGES_COUNT = 10m (FILMS_WATCHES * MESSAGE_PER_FILM)
FILMS_WATCHES = 100_000
MESSAGE_PER_FILM = 100

USERS_COUNT = 10_000
FILMS_COUNT = 1_000
WATCH_DATE = datetime.date(2022, 3, 1)


# Clickhouse
# clickhouse = Client(host='localhost', port=9000)

# Postgres
pg_conn = psycopg2.connect(
    host='localhost',
    port=5432,
    user='user',
    password='password',
    dbname='test_database',
    options='-c search_path=test_schema',
)
pg_cursor = pg_conn.cursor()

# Cassandra
# cs_cluster = Cluster(['localhost'])
# cs_session = cs_cluster.connect()


def main():
    user_uuids = [str(uuid.uuid4()) for _ in range(USERS_COUNT)]
    film_uuids = [str(uuid.uuid4()) for _ in range(FILMS_COUNT)]

    chunk = []
    for i in range(FILMS_WATCHES):
        film = random.choice(film_uuids)
        user = random.choice(user_uuids)
        date = WATCH_DATE
        for timestamp in range(0, MESSAGE_PER_FILM):
            chunk.append((film, user, date, timestamp))
            if len(chunk) >= CHUNK_SIZE:
                send_chunk(chunk)
    send_chunk(chunk)


def send_chunk(chunk: List):
    # send_chunk_to_clickhouse(chunk)
    send_chunk_to_postgres(chunk)
    # send_chunk_to_cassandra(chunk)
    chunk.clear()


def send_chunk_to_clickhouse(chunk: List):
    global clickhouse
    if chunk:
        start_time = time.time()
        clickhouse.execute("""INSERT INTO movie_watches (MovieID, UserID, ViewDate, ViewTimestamp) VALUES""", chunk)
        total_time = time.time() - start_time
        print(f'A chunk of {len(chunk):_} items was recorded to Clickhouse in {total_time:.5f} seconds.')


def send_chunk_to_postgres(chunk: List):
    global pg_conn
    global pg_cursor
    if chunk:
        query = """INSERT INTO movie_watches VALUES %s"""
        start_time = time.time()
        execute_values(pg_cursor, query, chunk, page_size=CHUNK_SIZE)
        pg_conn.commit()
        total_time = time.time() - start_time
        print(f'A chunk of {len(chunk):_} items was recorded to Postgres in {total_time:.5f} seconds.')


def send_chunk_to_cassandra(chunk: List):
    global cs_session

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    if chunk:
        query = cs_session.prepare("""INSERT INTO test_keyspace.movie_watches (id, movieid, userid, viewdate, viewtimestamp) VALUES (uuid(), ?, ?, ?, ?)""")
        start_time = time.time()
        # Касандра не может в большие чанки, приходится разбивать на маленькие
        for mini_chunk in chunks(chunk, 300):
            mini_chunk_start_time = time.time()
            for row in mini_chunk:
                batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
                batch.add(query, (uuid.UUID(row[0]), uuid.UUID(row[1]), row[2], row[3]))
                cs_session.execute(batch)
            mini_chunk_total_time = time.time() - mini_chunk_start_time
            print(f'A chunk of {len(mini_chunk):_} items was recorded to Cassandra in {mini_chunk_total_time:.5f} seconds.')
        total_time = time.time() - start_time
        print(f'A chunk of {len(chunk):_} items was recorded to Cassandra in {total_time:.5f} seconds.')


if __name__ == '__main__':
    main()
