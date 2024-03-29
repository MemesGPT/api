from __future__ import annotations
import asyncio
import logging

import aiohttp
import fastapi
import langchain.chat_models as langchain_chat_models
import openai
import sqlalchemy
import sqlalchemy.ext.asyncio as sqlalchemy_asyncio
import uvicorn

import lib.api.rest.v1.chatgpt4 as chatgpt_api
import lib.api.rest.v1.dalle as dalle_api
import lib.api.rest.v1.gigachat as gigachat_api
import lib.api.rest.v1.health as health_api
import lib.api.rest.v1.joke as joke_api
import lib.app.fastapi.errors as app_errors
import lib.app.fastapi.settings as app_settings
import lib.chatgpt.services as chatgpt_services
import lib.dalle.serveces as dalle_services
import lib.gigachat.clients as gigachat_clients
import lib.gigachat.services as gigachat_services
import lib.joke.repositories as joke_repositories
import lib.joke.sevices as joke_services
import lib.utils.sqlalchemy as sqlalchemy_utils

logger = logging.getLogger(__name__)


class Application:
    def __init__(
        self,
        settings: app_settings.Settings,
        fastapi_app: fastapi.FastAPI,
        aiohttp_client: aiohttp.ClientSession,
        sqlalchemy_engine: sqlalchemy_utils.AsyncEngine,
    ) -> None:
        self._settings = settings
        self._fastapi_app = fastapi_app
        self._aiohttp_client = aiohttp_client
        self._sqlalchemy_engine = sqlalchemy_engine

    @classmethod
    def from_settings(cls, settings: app_settings.Settings) -> Application:
        logging.basicConfig(
            level=settings.LOGS_MIN_LEVEL,
            format=settings.LOGS_FORMAT,
        )

        logger.info("Initializing application")

        logger.info("Creating sqlalchemy engine")
        sqlalchemy_url = sqlalchemy.engine.URL.create(
            drivername="postgresql+asyncpg",
            username=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.PG_MASTER_HOST,
            port=settings.PG_MASTER_PORT,
            database=settings.POSTGRES_DB,
        )
        sqlalchemy_engine = sqlalchemy_asyncio.create_async_engine(
            url=sqlalchemy_url,
            echo=settings.is_development,
            pool_size=settings.PG_CONNECTION_POOL_SIZE,
        )
        sqlalchemy_session_maker: sqlalchemy_utils.AsyncSessionMaker = sqlalchemy_asyncio.async_sessionmaker(
            bind=sqlalchemy_engine,
            class_=sqlalchemy_utils.AsyncSession,
        )

        logger.info("Initializing global clients")
        aiohttp_client = aiohttp.ClientSession()

        logger.info("Initializing local clients")
        gigachat_auth_client = gigachat_clients.GigachatAuthClient(
            provider=aiohttp_client,
            token=settings.GIGACHAT_API_KEY,
        )
        gigachat_art_client = gigachat_clients.GigachatArtClient(
            provider=aiohttp_client,
            auth_client=gigachat_auth_client,
        )
        dalle_client = openai.OpenAI(api_key=settings.openai.OPENAI_API_KEY.get_secret_value())

        logger.info("Initializing chat_models")
        openai_gpt4 = langchain_chat_models.ChatOpenAI(  # type: ignore
            model=settings.openai.DEF_GPT_4_MODEL,
            openai_api_key=settings.openai.OPENAI_API_KEY.get_secret_value(),
        )

        logger.info("Initializing repositories")
        joke_repository = joke_repositories.JokePostgresRepository()

        logger.info("Initializing services")
        dalle_service = dalle_services.DalleServece(dalle_client=dalle_client)
        chatgpt_service = chatgpt_services.ChatGPTServece(
            chatgpt_llm=openai_gpt4,
        )
        gigachat_service = gigachat_services.GigachatArtService(gigachat_client=gigachat_art_client)
        joke_service = joke_services.JokeService(
            joke_repository=joke_repository,
            session_maker=sqlalchemy_session_maker,
        )

        logger.info("Initializing handlers")
        liveness_probe_handler = health_api.LivenessProbeHandler()
        promt_create_handler = health_api.PromtCreateHandler()
        promt_detail_handler = health_api.PromtDetailHandler()
        dalle_create_handler = dalle_api.DalleCreateHandler(dalle_service=dalle_service)
        chatgpt_create_handler = chatgpt_api.ChatGPT4CreateHandler(chatgpt_service=chatgpt_service)
        gigachat_art_create_handler = gigachat_api.GigachatArtCreateHandler(gigachat_service=gigachat_service)
        joke_list_handler = joke_api.JokeListHandler(joke_service=joke_service)

        logger.info("Creating fastapi application")
        fastapi_app = fastapi.FastAPI()

        logger.info("Initializing routes")
        # ping
        fastapi_app.get("/api/v1/health/liveness", tags=["ping"])(liveness_probe_handler.process)
        fastapi_app.post("/api/v1/promt", tags=["ping"])(promt_create_handler.process)
        fastapi_app.get("/api/v1/promt/{promt_id}", tags=["ping"])(promt_detail_handler.process)

        # OpenAI
        fastapi_app.post("/api/v1/openai/chat", tags=["OpenAI"], name="gpt-4")(chatgpt_create_handler.process)
        fastapi_app.post("/api/v1/openai/dalle", tags=["OpenAI"])(dalle_create_handler.process)

        # Gigachat
        fastapi_app.post("/api/v1/gigachat/art", tags=["Gigachat"])(gigachat_art_create_handler.process)

        # Jokes
        fastapi_app.get("/api/v1/jokes", tags=["Jokes"])(joke_list_handler.process)

        logger.info("Creating application")
        application = Application(
            settings=settings,
            fastapi_app=fastapi_app,
            aiohttp_client=aiohttp_client,
            sqlalchemy_engine=sqlalchemy_engine,
        )

        logger.info("Initializing application finished")

        return application

    async def start(self) -> None:
        await self.start_app()

    async def start_app(self) -> None:
        logger.info("HTTP server is starting")

        try:
            server = uvicorn.Server(
                config=uvicorn.Config(
                    app=self._fastapi_app,
                    host=self._settings.SERVER_HOST,
                    port=self._settings.SERVER_PORT,
                ),
            )
            await server.serve()
        except asyncio.CancelledError:
            logger.info("HTTP server has been interrupted")
        except BaseException as unexpected_error:
            logger.exception("HTTP server failed to start")

            msg = "HTTP server failed to start"
            raise app_errors.StartServerError(msg) from unexpected_error

    async def dispose(self) -> None:
        logger.info("Application is shutting down...")

        dispose_errors: list = []

        logger.info("Disposing SQLAlchemy client")
        try:
            await self._sqlalchemy_engine.dispose()
        except Exception as unexpected_error:
            dispose_errors.append(unexpected_error)
            logger.exception("Failed to dispose SQLAlchemy client")
        else:
            logger.info("SQLAlchemy client has been disposed")

        logger.info("Disposing Aiohttp client")
        try:
            await self._aiohttp_client.close()
        except Exception as unexpected_error:
            dispose_errors.append(unexpected_error)
            logger.exception("Failed to dispose Aiohttp client")
        else:
            logger.info("Aiohttp client has been disposed")

        if len(dispose_errors) != 0:
            logger.error("Application has shut down with errors")
            msg = "Application has shut down with errors, see logs above"
            raise app_errors.DisposeError(msg)

        logger.info("Application has successfully shut down")


__all__ = [
    "Application",
]
