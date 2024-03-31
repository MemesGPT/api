import http
import pathlib
import typing
import uuid

import aiofiles
import aiohttp

import lib.dalle.serveces as dalle_services
import lib.joke.models as joke_models
import lib.joke.repositories.postgres as joke_repositories
import lib.utils.sqlalchemy as sqlalchemy_utils


class JokeServiceProtocol(typing.Protocol):
    class NotFoundError(Exception):
        ...

    class DownloadImageError(Exception):
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
        user: joke_models.JokeCreate,
    ) -> joke_models.Joke:
        ...


class JokeService(JokeServiceProtocol):
    def __init__(
        self,
        provider: aiohttp.ClientSession,
        joke_repository: joke_repositories.JokePostgresRepositoryProtocol,
        session_maker: sqlalchemy_utils.AsyncSessionMaker,
        dalle_service: dalle_services.DalleServiceProtocol,
    ) -> None:
        self._provider = provider
        self._joke_repository = joke_repository
        self._session_maker = session_maker
        self._dalle_service = dalle_service

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
        joke: joke_models.JokeCreate,
    ) -> joke_models.Joke:
        async with self._session_maker() as session:
            joke_result = await self._joke_repository.create(session, joke)

            image_url = await self._dalle_service.create(promt_str=joke.text_final)
            image_path = await self._download_image(image_url=image_url, image_name=joke_result.joke_id)

            await session.commit()
        return joke_models.Joke(
            joke_id=joke_result.joke_id,
            text_final=joke.text_final,
            image_id=image_path,
        )

    async def _download_image(self, image_url: str, image_name: str) -> str:
        image_path = pathlib.PurePath("/media/raid/memes_files", image_name)
        async with self._provider.get(image_url) as response:
            if response.status != http.HTTPStatus.OK:
                raise self.DownloadImageError
            data = await response.read()
            async with aiofiles.open(image_path, "wb") as file:
                await file.write(data)
                return image_path.name


__all__ = [
    "JokeService",
    "JokeServiceProtocol",
]
