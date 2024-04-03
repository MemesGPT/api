import dataclasses
import uuid


@dataclasses.dataclass
class JokeCreate:
    prompt_text: str


@dataclasses.dataclass
class JokeWithoutID:
    text_final: str
    image_id: str | None = None


@dataclasses.dataclass
class Joke:
    joke_id: uuid.UUID
    text_final: str
    image_id: str | None = None


__all__ = [
    "Joke",
    "JokeWithoutID",
    "JokeCreate",
]
