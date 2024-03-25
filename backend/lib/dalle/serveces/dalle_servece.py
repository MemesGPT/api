import logging
import typing

import openai

import lib.dalle.schemes as dalle_schemes

logger = logging.getLogger(__name__)


class DalleServiceProtocol(typing.Protocol):
    async def create(self, promt_str: str) -> str | None:
        ...


class DalleServece(DalleServiceProtocol):
    def __init__(self, dalle_client: openai.OpenAI) -> None:
        self._dalle_client = dalle_client

    async def create(self, promt_str: str) -> str | None:
        response = self._dalle_client.images.generate(**dalle_schemes.ImagesGenerateScheme(prompt=promt_str).dict())
        return response.data[0].url


__all__ = [
    "DalleServece",
    "DalleServiceProtocol",
]
