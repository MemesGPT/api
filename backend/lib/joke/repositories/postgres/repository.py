import dataclasses
import typing
import uuid

import sqlalchemy

import lib.joke.models as joke_models
import lib.joke.repositories.postgres.models as repository_models
import lib.utils.sqlalchemy as sqlalchemy_utils


class JokePostgresRepositoryProtocol(typing.Protocol):
    class NotFoundError(Exception):
        ...

    async def get_all(self, session: sqlalchemy_utils.AsyncSession) -> list[joke_models.Joke]:
        ...

    async def get_by_id(
        self,
        session: sqlalchemy_utils.AsyncSession,
        entity_id: uuid.UUID,
    ) -> joke_models.Joke:
        """Raise NotFoundError - when user not found."""
        ...

    async def create(
        self,
        session: sqlalchemy_utils.AsyncSession,
        joke: joke_models.JokeWithoutID,
    ) -> joke_models.Joke:
        ...


class JokePostgresRepository(JokePostgresRepositoryProtocol):
    async def get_all(self, session: sqlalchemy_utils.AsyncSession) -> list[joke_models.Joke]:
        query = sqlalchemy.select(repository_models.Joke)
        result: sqlalchemy.engine.Result = await session.execute(query)
        jokes: typing.Sequence[repository_models.Joke] = result.scalars().all()
        return [joke_models.Joke(**joke.as_dict()) for joke in jokes]

    async def get_by_id(
        self,
        session: sqlalchemy_utils.AsyncSession,
        entity_id: uuid.UUID,
    ) -> joke_models.Joke:
        query = sqlalchemy.select(repository_models.Joke).where(repository_models.Joke.joke_id == entity_id)
        result: sqlalchemy.engine.Result = await session.execute(query)
        joke: repository_models.Joke | None = result.scalars().one_or_none()

        if joke is None:
            raise self.NotFoundError

        return joke_models.Joke(**joke.as_dict())

    async def create(
        self,
        session: sqlalchemy_utils.AsyncSession,
        joke: joke_models.JokeWithoutID,
    ) -> joke_models.Joke:
        db_user = repository_models.Joke(**dataclasses.asdict(joke))
        session.add(db_user)
        await session.flush()

        return joke_models.Joke(**db_user.as_dict())  # pylint: disable=not-a-mapping


__all__ = [
    "JokePostgresRepository",
    "JokePostgresRepositoryProtocol",
]
