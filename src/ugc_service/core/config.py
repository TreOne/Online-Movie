import os
from logging import config as logging_config

import sentry_sdk

from .logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Настройки проекта.
PROJECT_NAME: str = 'Сервис UGC'
PROJECT_DESCRIPTION: str = 'OLTP хранилище'
PROJECT_VERSION: str = '1.0'
PROJECT_LICENSE_INFO: dict[str, str] = {
    'name': 'Apache 2.0',
    'url': 'https://www.apache.org/licenses/LICENSE-2.0.html',
}

# env Variable
KAFKA_BOOTSTRAP_SERVERS: str = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC: str = os.getenv('KAFKA_TOPIC', 'movie_watches')
KAFKA_REQUEST_TIMEOUT_MS: int = int(os.getenv('KAFKA_REQUEST_TIMEOUT_MS', 5000))

# JWT
jwt_secret_key: str = os.getenv('JWT_SECRET_KEY', 'buz')
jwt_algorithms: list[str] = ['HS256']

# Sentry
SENTRY_DSN: str = os.getenv('SENTRY_DSN')

if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN)
