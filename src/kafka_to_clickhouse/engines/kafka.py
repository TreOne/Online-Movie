from confluent_kafka import Consumer
from settings.settings import KafkaSettings


def get_consumer(settings: KafkaSettings) -> Consumer:
    consumer = Consumer({
        'bootstrap.servers': settings.bootstrap_servers,
        'group.id': settings.group_id,
        'auto.offset.reset': settings.auto_offset_reset,
        'enable.auto.commit': settings.enable_auto_commit,
    })
    return consumer
