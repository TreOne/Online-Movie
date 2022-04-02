from typing import Optional

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FastJsonModel(BaseModel):
    """Модель с быстрым json-сериализатором."""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Response(FastJsonModel):
    """Страница результатов с пагинацией."""

    msg: Optional[str] = Field(title="Сообщение от сервера.", example="OK")
