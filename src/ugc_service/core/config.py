import asyncio
import os
from logging import config as logging_config

from .logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Настройки проекта.
PROJECT_NAME = 'Сервис UGC'
PROJECT_DESCRIPTION = 'OLTP хранилище'
PROJECT_VERSION = '1.0'
PROJECT_LICENSE_INFO = {
    'name': 'Apache 2.0',
    'url': 'https://www.apache.org/licenses/LICENSE-2.0.html',
}

# env Variable
KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9093")
KAFKA_TOPIC: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "user_id_movie_id")
KAFKA_CONSUMER_GROUP: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "group-id")
KAFKA_REQUEST_TIMEOUT_MS: int = 5000

# JWT
jwt_secret_key = os.getenv('SECRET_KEY', 'buz')
jwt_algorithms = ['HS256']
