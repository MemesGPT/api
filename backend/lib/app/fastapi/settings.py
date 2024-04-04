import dataclasses
import typing

import pydantic

LogLevel = typing.Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


@dataclasses.dataclass
class HTTPEndpoint:
    path: str
    method: str


class OpenAISettings(pydantic.BaseSettings):
    OPENAI_API_KEY: pydantic.SecretStr
    DEF_TEMPERATURE: float = 0.9
    DEF_GPT_4_MODEL: str = "gpt-4"


class Settings(pydantic.BaseSettings):
    # App
    APP_ENV: str = "development"
    APP_NAME: str = "memes-gpt/backend"
    APP_VERSION: str = "0.0.1"

    # Logging
    LOGS_MIN_LEVEL: LogLevel = "DEBUG"
    LOGS_FORMAT: str = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"

    # Server
    SERVER_HOST: str
    SERVER_PORT: int

    # OpenAI
    openai: OpenAISettings = OpenAISettings()

    # GigaChat
    GIGACHAT_API_KEY: str

    # PostgreSQL
    PG_MASTER_HOST: str = "127.0.0.1"
    PG_MASTER_PORT: int = 50432
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    PG_CONNECTION_POOL_SIZE: int = 100

    # files path
    DALLE_IMG_DIR: str = "/var/www/memes_images"
    MEMES_IMG_BASE_URL: str

    DEF_PAGE_NUMBER: int = 1
    DEF_PAGE_SIZE: int = 50

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"


__all__ = [
    "Settings",
]
