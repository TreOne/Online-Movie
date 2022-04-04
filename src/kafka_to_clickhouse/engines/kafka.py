from confluent_kafka import Consumer


def get_consumer():
    consumer = Consumer({
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'movie_watches',
        'auto.offset.reset': 'earliest',
    })
    consumer.subscribe(topics=['movie_watches'])
    return consumer
