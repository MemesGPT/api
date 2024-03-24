import logging
import typing

from openai import OpenAI

logger = logging.getLogger(__name__)


class DalleServiceProtocol(typing.Protocol):
    async def create(self, promt_str: str) -> str | None:
        ...


class DalleServece(DalleServiceProtocol):
    def __init__(self, dalle_client: OpenAI) -> None:
        self._dalle_client = dalle_client

    async def create(self, promt_str: str) -> str | None:
        response = self._dalle_client.images.generate(
            model="dall-e-3",
            prompt=promt_str,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url


__all__ = [
    "DalleServece",
    "DalleServiceProtocol",
]
