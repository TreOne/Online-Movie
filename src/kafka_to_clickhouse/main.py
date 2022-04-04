from clickhouse_driver import Client
from confluent_kafka import Consumer

from data_structures.movie_watch import MovieWatch
from engines.click_house import get_client
from engines.kafka import get_consumer


def main():
    kafka: Consumer = get_consumer()
    clickhouse: Client = get_client()

    messages = kafka.consume(num_messages=100_000, timeout=5.0)
    watches = []
    for message in messages:
        if not message:
            break
        watch = MovieWatch.create_from_message(message)
        watches.append(watch)

    if watches:
        print(f'Messages received: {len(watches)}')
        data = [watch.to_clickhouse() for watch in watches]
        clickhouse.execute("""INSERT INTO movie_watches (MovieID, UserID, ViewDate, ViewTimestamp) VALUES""", data)

    kafka.close()
    clickhouse.disconnect()


if __name__ == '__main__':
    main()
