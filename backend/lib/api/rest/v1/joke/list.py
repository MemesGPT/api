import dataclasses
import typing

import lib.api.rest.v1.joke.schemes as joke_schemes
import lib.joke.sevices as joke_services


class JokeListHandlerProtocol(typing.Protocol):
    async def process(self) -> joke_schemes.PaginateJokesScheme:
        ...


class JokeListHandler(JokeListHandlerProtocol):
    def __init__(
        self,
        joke_service: joke_services.JokeServiceProtocol,
    ) -> None:
        self._joke_service = joke_service

    async def process(self) -> joke_schemes.PaginateJokesScheme:
        jokes = await self._joke_service.get_all()
        return joke_schemes.PaginateJokesScheme(
            page={
                "total_pages": 1,
                "total_items": 1,
                "number": 1,
                "size": 1,
            },
            results=[joke_schemes.JokeScheme.parse_obj(dataclasses.asdict(joke)) for joke in jokes],
        )


__all__ = [
    "JokeListHandler",
    "JokeListHandlerProtocol",
]
