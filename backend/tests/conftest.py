import asyncio
import typing

import fastapi.testclient as fastapi_pytest_plugin
import pytest
import pytest_asyncio

import lib.app.fastapi as app
import lib.app.fastapi.settings as app_settings
import tests.functional.utils.types as test_utils_types

pytest_plugins = "tests.functional.fixtures"


@pytest.fixture(scope="session", name="loop")
def fixture_loop(event_loop: asyncio.AbstractEventLoop) -> asyncio.AbstractEventLoop:
    return event_loop


@pytest.fixture(scope="session", name="settings")
def fixture_settings() -> app_settings.Settings:
    return app_settings.Settings()


@pytest_asyncio.fixture(scope="session", name="application")
async def fixture_application(
    settings: app_settings.Settings,
) -> typing.AsyncGenerator[app.Application, None]:
    application = app.Application.from_settings(settings)

    yield application

    await application.dispose()


@pytest.fixture(name="http_client")
def fixture_http_client(
    application: app.Application,
) -> test_utils_types.TestClient:
    return fastapi_pytest_plugin.TestClient(application._fastapi_app)  # noqa: SLF001
