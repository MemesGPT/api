import dataclasses
import typing

import pydantic_settings

LogLevel = typing.Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


@dataclasses.dataclass
class HTTPEndpoint:
    path: str
    method: str


class Settings(pydantic_settings.BaseSettings):
    # App
    APP_ENV: str = "development"
    APP_NAME: str = "memes-gpt/backend"
    APP_VERSION: str = "0.0.1"

    # Logging
    LOGS_MIN_LEVEL: LogLevel = "DEBUG"
    LOGS_FORMAT: str = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"

    # Server
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8081

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"


__all__ = [
    "Settings",
]
