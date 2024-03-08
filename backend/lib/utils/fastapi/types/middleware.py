import typing

import fastapi


class CallNextProtocol(typing.Protocol):
    async def __call__(self, request: fastapi.Request) -> fastapi.Response:
        ...


class MiddlewareProtocol(typing.Protocol):
    async def process(
        self,
        request: fastapi.Request,
        call_next: CallNextProtocol,
    ) -> fastapi.Response:
        ...


__all__ = [
    "CallNextProtocol",
    "MiddlewareProtocol",
]
