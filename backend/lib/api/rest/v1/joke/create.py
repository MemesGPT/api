import dataclasses
import typing

import lib.api.rest.v1.joke.schemes as joke_schemes
import lib.dalle.serveces as dalle_serveces
import lib.joke.models as joke_models
import lib.joke.sevices as joke_services


class CreateJokeHandlerProtocol(typing.Protocol):
    async def process(self, promt: joke_schemes.JokeCreateScheme) -> joke_schemes.JokeScheme:
        ...


class CreateJokeHandler(CreateJokeHandlerProtocol):
    def __init__(
        self,
        joke_service: joke_services.JokeServiceProtocol,
        dalle_service: dalle_serveces.DalleServiceProtocol,
    ) -> None:
        self._joke_service = joke_service
        self._dalle_service = dalle_service

    async def process(self, promt: joke_schemes.JokeCreateScheme) -> joke_schemes.JokeScheme:
        joke = await self._joke_service.create(joke_models.JokeCreate(text_final=promt.text))
        return joke_schemes.JokeScheme(**dataclasses.asdict(joke))
