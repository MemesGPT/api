import typing
import uuid

import lib.joke.models as joke_models
import lib.joke.repositories.postgres as joke_repositories
import lib.utils.sqlalchemy as sqlalchemy_utils


class JokeServiceProtocol(typing.Protocol):
    class NotFoundError(Exception):
        ...

    async def get_all(self) -> list[joke_models.Joke]:
        ...

    async def get_by_id(
        self,
        entity_id: uuid.UUID,
    ) -> joke_models.Joke:
        """Raise NotFoundError - when user not found."""
        ...

    async def create(
        self,
        user: joke_models.JokeWithoutID,
    ) -> joke_models.Joke:
        ...


class JokeService(JokeServiceProtocol):
    def __init__(
        self,
        joke_repository: joke_repositories.JokePostgresRepositoryProtocol,
        session_maker: sqlalchemy_utils.AsyncSessionMaker,
    ) -> None:
        self._joke_repository = joke_repository
        self._session_maker = session_maker

    async def get_all(self) -> list[joke_models.Joke]:
        async with self._session_maker() as session:
            return await self._joke_repository.get_all(session)

    async def get_by_id(
        self,
        entity_id: uuid.UUID,
    ) -> joke_models.Joke:
        async with self._session_maker() as session:
            return await self._joke_repository.get_by_id(session, entity_id)

    async def create(
        self,
        user: joke_models.JokeWithoutID,
    ) -> joke_models.Joke:
        async with self._session_maker() as session:
            result = await self._joke_repository.create(session, user)
            await session.commit()
            return result


__all__ = [
    "JokeService",
    "JokeServiceProtocol",
]
