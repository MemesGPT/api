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

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"


__all__ = [
    "Settings",
]
