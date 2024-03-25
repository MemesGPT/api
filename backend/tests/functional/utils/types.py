import typing

import fastapi
import fastapi.testclient as fastapi_test

TestClient = fastapi_test.TestClient


class FastAPIClientFactory(typing.Protocol):
    async def __call__(self, app: fastapi.FastAPI) -> TestClient:
        ...


__all__ = [
    "FastAPIClientFactory",
    "TestClient",
]
