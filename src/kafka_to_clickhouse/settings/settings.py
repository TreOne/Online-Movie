from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, BaseSettings


class CliclHouseSettings(BaseModel):
    host: str
    port: int


class KafkaSettings(BaseModel):
    topic: str
    host: str
    port: int


def yaml_settings_source(settings: BaseSettings) -> dict[str, Any]:
    """Возвращает настройки из файла settings.yaml."""
    settings_path = Path(__file__).parent / 'settings.yaml'
    with settings_path.open('r', encoding='utf-8') as f:
        yaml_settings = yaml.load(f, Loader=yaml.Loader)
    return yaml_settings
