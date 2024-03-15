import typing

import lib.api.rest.v1.dalle.schemes as dalle_schemes
import lib.dalle.serveces as dalle_serveces


class DalleCreateHandlerProtocol(typing.Protocol):
    class NotCreatedError(Exception):
        ...

    async def process(self, promt_in: dalle_schemes.DallePromtScheme) -> dalle_schemes.ImageScheme:
        ...


class DalleCreateHandler(DalleCreateHandlerProtocol):
    def __init__(self, dalle_service: dalle_serveces.DalleServiceProtocol) -> None:
        self._dalle_service = dalle_service

    async def process(self, promt_in: dalle_schemes.DallePromtScheme) -> dalle_schemes.ImageScheme:
        image_url = await self._dalle_service.create(promt_in.text)
        return dalle_schemes.ImageScheme(
            image_url=image_url,
        )


__all__ = [
    "DalleCreateHandler",
    "DalleCreateHandlerProtocol",
]
