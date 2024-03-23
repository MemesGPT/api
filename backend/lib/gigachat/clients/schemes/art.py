import uuid

import pydantic

import lib.gigachat.config as gigachat_configs

gigachat_config = gigachat_configs.GigachatConfig()


class UserMessageScheme(pydantic.BaseModel):
    role: str = "user"
    content: str


class ArtMessageScheme(pydantic.BaseModel):
    model: str = gigachat_config.default_model
    messages: list[UserMessageScheme] = []
    temperature:  float = gigachat_config.default_temperature
    top_p: float = gigachat_config.default_top_p
    n: int = gigachat_config.default_n
    stream: bool = gigachat_config.default_stream
    max_tokens: int = gigachat_config.default_max_tokens
    repetition_penalty: int = gigachat_config.default_repetition_penalty
    update_interval: int = gigachat_config.default_update_interval


class HeaderFetchImageIdScheme(pydantic.BaseModel):
    content_type: str = pydantic.Field(default="application/json", alias="Content-Type")
    accept: str = pydantic.Field(default="application/json", alias="Accept")
    authorization: str = pydantic.Field(..., alias="Authorization")

    class Config:
        allow_population_by_field_name = True


class HeaderFetchImageScheme(pydantic.BaseModel):
    accept: str = pydantic.Field(default="application/json", alias="Accept")
    authorization: str = pydantic.Field(..., alias="Authorization")

    class Config:
        allow_population_by_field_name = True


class HeaderFetchTokenScheme(pydantic.BaseModel):
    content_type: str = pydantic.Field(default="application/x-www-form-urlencoded", alias="Content-Type")
    accept: str = pydantic.Field(default="application/json", alias="Accept")
    rquid: uuid.UUID = pydantic.Field(default=uuid.uuid4(), alias="RqUID")
    authorization: str = pydantic.Field(..., alias="Authorization")

    class Config:
        allow_population_by_field_name = True


__all__ = [
    "ArtMessageScheme",
    "UserMessageScheme",
    "HeaderFetchImageIdScheme",
    "HeaderFetchImageScheme",
    "HeaderFetchTokenScheme",
]
