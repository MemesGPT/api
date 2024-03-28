import uuid

import pydantic


class JokeWithoutIdScheme(pydantic.BaseModel):
    text_final: str
    image_id: str


class JokeScheme(JokeWithoutIdScheme):
    joke_id: uuid.UUID


__all__ = [
    "JokeScheme",
    "JokeWithoutIdScheme",
]
