import asyncio
import typing

import pytest


@pytest.fixture(scope="session", name="event_loop")
def fixture_event_loop() -> typing.Generator[asyncio.AbstractEventLoop, typing.Any, None]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


__all__ = [
    "fixture_event_loop",
]
