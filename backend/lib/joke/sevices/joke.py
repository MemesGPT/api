import http
import pathlib
import typing
import uuid

import aiofiles
import aiohttp

import lib.chatgpt.services as chatgpt_services
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

    async def create_joke(
        self,
        joke: joke_models.JokeCreate,
    ) -> joke_models.Joke:
        ...

    async def create_image(
        self,
        image_prompt: str,
        joke_id: uuid.UUID,
    ) -> joke_models.Joke:
        ...


class JokeService(JokeServiceProtocol):
    def __init__(  # noqa: PLR0913
        self,
        provider: aiohttp.ClientSession,
        joke_repository: joke_repositories.JokePostgresRepositoryProtocol,
        session_maker: sqlalchemy_utils.AsyncSessionMaker,
        dalle_service: dalle_services.DalleServiceProtocol,
        chatgpt_service: chatgpt_services.ChatGPTServeceProtocol,
    ) -> None:
        self._provider = provider
        self._joke_repository = joke_repository
        self._session_maker = session_maker
        self._dalle_service = dalle_service
        self._chatgpt_service = chatgpt_service

    async def get_all(self) -> list[joke_models.Joke]:
        async with self._session_maker() as session:
            return await self._joke_repository.get_all(session)

    async def get_by_id(
        self,
        entity_id: uuid.UUID,
    ) -> joke_models.Joke:
        async with self._session_maker() as session:
            return await self._joke_repository.get_by_id(session, entity_id)

    async def create_joke(
        self,
        joke: joke_models.JokeCreate,
    ) -> joke_models.Joke:
        joke_text = await self._chatgpt_service.create(promt_str=joke.prompt_text)
        joke_obj = joke_models.JokeWithoutID(text_final=joke_text)
        async with self._session_maker() as session:
            joke_result = await self._joke_repository.create(session, joke_obj)
            await session.commit()
        return joke_models.Joke(
            joke_id=joke_result.joke_id,
            text_final=joke_result.text_final,
        )

    async def create_image(
        self,
        image_prompt: str,
        joke_id: uuid.UUID,
    ) -> joke_models.Joke:
        ...

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
