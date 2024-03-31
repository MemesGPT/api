import uuid

import pydantic

import lib.api.rest.v1.schemes as base_schemes


class JokeCreateScheme(pydantic.BaseModel):
    text_final: str = pydantic.Field(..., alias="text")


class JokeWithoutIdScheme(JokeCreateScheme):
    text_final: str = pydantic.Field(..., alias="text")
    image_id: str = pydantic.Field(..., alias="image")


class JokeScheme(JokeWithoutIdScheme):
    joke_id: uuid.UUID = pydantic.Field(..., alias="id")

    class Config:
        allow_population_by_field_name = True


class PaginateJokesScheme(pydantic.BaseModel):
    page: base_schemes.Paginator
    results: list[JokeScheme]


__all__ = [
    "JokeScheme",
    "JokeWithoutIdScheme",
    "JokeCreateScheme",
    "PaginateJokesScheme",
]
