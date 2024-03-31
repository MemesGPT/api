import uuid

import pydantic


class JokeCreateScheme(pydantic.BaseModel):
    text_final: str = pydantic.Field(..., alias="text")


class JokeWithoutIdScheme(JokeCreateScheme):
    text_final: str = pydantic.Field(..., alias="text")
    image_id: str = pydantic.Field(..., alias="image")


class JokeScheme(JokeWithoutIdScheme):
    joke_id: uuid.UUID = pydantic.Field(..., alias="id")


__all__ = [
    "JokeScheme",
    "JokeWithoutIdScheme",
    "JokeCreateScheme",
]
