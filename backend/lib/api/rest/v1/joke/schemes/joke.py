import uuid

import pydantic


class JokeCreateScheme(pydantic.BaseModel):
    text: str


class JokeWithoutIdScheme(JokeCreateScheme):
    text_final: str
    image_id: str


class JokeScheme(JokeWithoutIdScheme):
    joke_id: uuid.UUID


__all__ = [
    "JokeScheme",
    "JokeWithoutIdScheme",
    "JokeCreateScheme",
]
