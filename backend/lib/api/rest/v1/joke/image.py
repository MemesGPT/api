import dataclasses
import typing
import uuid

import lib.api.rest.v1.joke.schemes as joke_schemes
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
        joke = await self._joke_service.create_image(image_prompt=prompt.text_final, joke_id=mem_id)
        return joke_schemes.JokeScheme(**dataclasses.asdict(joke))


__all__ = [
    "CreateImageHandler",
    "CreateImageHandlerProtocol",
]
