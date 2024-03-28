import typing
import uuid

import lib.api.rest.v1.joke.schemes as joke_schemes
import lib.joke.sevices as joke_services


class JokeListHandlerProtocol(typing.Protocol):
    async def process(self) -> list[joke_schemes.JokeScheme]:
        ...


class JokeListHandler(JokeListHandlerProtocol):
    def __init__(
        self,
        joke_service: joke_services.JokeServiceProtocol,
    ) -> None:
        self._joke_service = joke_service

    async def process(self) -> list[joke_schemes.JokeScheme]:
        return [joke_schemes.JokeScheme(
            joke_id=uuid.uuid4(),
            text_final="111",
            image_id="222",
        )]


__all__ = [
    "JokeListHandler",
    "JokeListHandlerProtocol",
]
