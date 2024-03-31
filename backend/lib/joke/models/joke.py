import dataclasses
import uuid


@dataclasses.dataclass
class JokeCreate:
    text_final: str


@dataclasses.dataclass
class JokeWithoutID(JokeCreate):
    image_id: str


@dataclasses.dataclass
class Joke(JokeWithoutID):
    joke_id: uuid.UUID


__all__ = [
    "Joke",
    "JokeWithoutID",
    "JokeCreate",
]
