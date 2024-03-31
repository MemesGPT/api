import dataclasses
import typing
import uuid

import lib.api.rest.v1.joke.schemes as joke_schemes
import lib.joke.models as joke_models
import lib.joke.sevices as joke_services


class CreateImageHandlerProtocol(typing.Protocol):
    async def process(self, mem_id: uuid.UUID, promt: joke_schemes.JokeCreateScheme) -> joke_schemes.JokeScheme:
        ...


class CreateImageHandler(CreateImageHandlerProtocol):
    def __init__(
        self,
        joke_service: joke_services.JokeServiceProtocol,
    ) -> None:
        self._joke_service = joke_service

    async def process(self, mem_id: uuid.UUID, prompt: joke_schemes.JokeCreateScheme) -> joke_schemes.JokeScheme:
        joke = await self._joke_service.create(joke_models.JokeCreate(text_final=prompt.text_final))
        return joke_schemes.JokeScheme(**dataclasses.asdict(joke))


__all__ = [
    "CreateImageHandler",
    "CreateImageHandlerProtocol",
]
