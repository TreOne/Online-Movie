from pathlib import Path
from typing import Any, Type

import yaml
from etl_tasks.abc_data_structure import TransferClass
from pydantic import BaseModel, BaseSettings, FilePath


class KafkaSettings(BaseModel):
    bootstrap_servers: str
    auto_offset_reset: str
    enable_auto_commit: str
    group_id: str


class ClickHouseSettings(BaseModel):
    host: str


class KafkaTaskSettings(BaseModel):
    topics: list[str]


class ClickHouseTaskSettings(BaseModel):
    table: str
    table_ddl: FilePath


class TaskSettings(BaseModel):
    task_name: str
    num_messages: int
    data_class: Type[TransferClass]
    kafka: KafkaTaskSettings
    clickhouse: ClickHouseTaskSettings

    class Config:
        arbitrary_types_allowed = True


class Settings(BaseSettings):
    kafka: KafkaSettings
    clickhouse: ClickHouseSettings
    tasks: list[TaskSettings]

    class Config:
        env_nested_delimiter = '__'
        case_sensitive = False

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            """Переопределение старшинства источников настроек."""
            return (
                init_settings,
                env_settings,
                yaml_settings_source,
                file_secret_settings,
            )


def yaml_settings_source(settings: BaseSettings) -> dict[str, Any]:
    """Возвращает настройки из файла settings.yaml."""
    settings_path = Path(__file__).parent / 'settings.yaml'
    with settings_path.open('r', encoding='utf-8') as f:
        yaml_settings = yaml.load(f, Loader=yaml.Loader)
    return yaml_settings
