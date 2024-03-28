import dataclasses
import uuid


@dataclasses.dataclass
class JokeWithoutID:
    image_id: str
    text_final: str


@dataclasses.dataclass
class Joke(JokeWithoutID):
    joke_id: uuid.UUID


__all__ = [
    "Joke",
    "JokeWithoutID",
]
