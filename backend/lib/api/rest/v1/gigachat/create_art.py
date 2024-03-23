import typing

import fastapi

import lib.api.rest.v1.gigachat.schemes as gigachat_schemes
import lib.gigachat.services as gigachat_services


class GigachatArtCreateHandlerProtocol(typing.Protocol):
    class NotCreatedError(Exception):
        ...

    async def process(self, promt_in: gigachat_schemes.GigachatArtPromtScheme) -> fastapi.Response:
        ...


class GigachatArtCreateHandler(GigachatArtCreateHandlerProtocol):
    def __init__(self, gigachat_service: gigachat_services.GigachatArtServiceProtocol) -> None:
        self._gigachat_service = gigachat_service

    async def process(self, promt_in: gigachat_schemes.GigachatArtPromtScheme) -> fastapi.Response:
        image_bytes = await self._gigachat_service.create(promt_str=promt_in.text)
        return fastapi.Response(content=image_bytes, media_type="image/jpg")


__all__ = [
    "GigachatArtCreateHandler",
    "GigachatArtCreateHandlerProtocol",
]
