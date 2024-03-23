import asyncio
import typing

import pytest
import pytest_asyncio
import aiohttp.pytest_plugin as aiohttp_pytest_plugin

from server import init_app
from fastapi.testclient import TestClient
import tests.functional.utils.types as test_utils_types

pytest_plugins = "tests.functional.fixtures"
aiohttp_client = aiohttp_pytest_plugin.aiohttp_client


@pytest.fixture(scope="session", name="loop")
def fixture_loop(event_loop: asyncio.AbstractEventLoop) -> asyncio.AbstractEventLoop:
    return event_loop


@pytest.fixture(scope="session", name="event_loop")
def fixture_event_loop() -> typing.Generator[asyncio.AbstractEventLoop, typing.Any, None]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="http_client")
async def fixture_http_client(
    aiohttp_client: test_utils_types.AioHTTPClientFactory,
) -> test_utils_types.TestClient:
    app = await init_app()
    return await aiohttp_client(app)
