import dataclasses
import typing

import lib.api.rest.v1.joke.schemes as joke_schemes
import lib.joke.models as joke_models
import lib.joke.sevices as joke_services


class CreateJokeHandlerProtocol(typing.Protocol):
    async def process(self, promt: joke_schemes.JokeCreateScheme) -> joke_schemes.JokeScheme:
        ...


class CreateJokeHandler(CreateJokeHandlerProtocol):
    def __init__(
        self,
        joke_service: joke_services.JokeServiceProtocol,
    ) -> None:
        self._joke_service = joke_service

    async def process(self, prompt: joke_schemes.JokeCreateScheme) -> joke_schemes.JokeScheme:
        joke = await self._joke_service.create_joke(joke_models.JokeCreate(prompt_text=prompt.text_final))
        return joke_schemes.JokeScheme(**dataclasses.asdict(joke))


__all__ = [
    "CreateJokeHandler",
    "CreateJokeHandlerProtocol",
]
