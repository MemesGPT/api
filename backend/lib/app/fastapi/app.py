from __future__ import annotations
import asyncio
import logging

import fastapi
import uvicorn
from langchain.chat_models import ChatOpenAI, GigaChat
from langchain.prompts import ChatPromptTemplate
from langserve import add_routes

import lib.api.rest.v1.health as health_api
import lib.api.rest.v1.promt as promt_api
import lib.app.fastapi.errors as app_errors
import lib.app.fastapi.settings as app_settings

logger = logging.getLogger(__name__)


class Application:
    def __init__(
        self,
        settings: app_settings.Settings,
        fastapi_app: fastapi.FastAPI,
    ) -> None:
        self._settings = settings
        self._fastapi_app = fastapi_app

    @classmethod
    def from_settings(cls, settings: app_settings.Settings) -> Application:
        logging.basicConfig(
            level=settings.LOGS_MIN_LEVEL,
            format=settings.LOGS_FORMAT,
        )

        logger.info("Initializing application")

        logger.info("Initializing handlers")
        liveness_probe_handler = health_api.LivenessProbeHandler()
        promt_detail_handler = promt_api.PromtDetailHandler()
        promt_create_handler = promt_api.PromtCreateHandler()

        logger.info("Creating fastapi application")
        fastapi_app = fastapi.FastAPI()

        logger.info("Initializing routes")
        # ping
        fastapi_app.get("/api/v1/health/liveness", tags=["ping"])(liveness_probe_handler.process)
        # promt
        fastapi_app.post("/api/v1/promt", tags=["promt"])(promt_create_handler.process)
        fastapi_app.get("/api/v1/promt/{promt_id}", tags=["promt"])(promt_detail_handler.process)

        add_routes(
            app=fastapi_app,
            runnable=GigaChat(credentials=settings.GIGACHAT_API_KEY, scope="GIGACHAT_API_PERS", verify_ssl_certs=False),
            path="/gigachat",
        )

        add_routes(
            fastapi_app,
            ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY),
            path="/openai",
        )

        prompt = ChatPromptTemplate.from_template("расскажи шутку о {topic}")
        add_routes(
            app=fastapi_app,
            runnable=prompt,
            path="/joke",
        )

        add_routes(
            app=fastapi_app,
            runnable=GigaChat(credentials=settings.GIGACHAT_API_KEY, scope="GIGACHAT_API_PERS", verify_ssl_certs=False),
            path="/my_runnable",
        )

        logger.info("Creating application")
        application = Application(
            settings=settings,
            fastapi_app=fastapi_app,
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

        if len(dispose_errors) != 0:
            logger.error("Application has shut down with errors")
            msg = "Application has shut down with errors, see logs above"
            raise app_errors.DisposeError(msg)

        logger.info("Application has successfully shut down")


__all__ = [
    "Application",
]
