import typing

import fastapi


class HandlerProtocol(typing.Protocol):
    async def process(self, request: fastapi.Request) -> fastapi.Response:
        ...


__all__ = [
    "HandlerProtocol",
]
