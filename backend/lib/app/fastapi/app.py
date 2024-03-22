from __future__ import annotations
import asyncio
import logging

import fastapi
import langchain_openai
import uvicorn

import lib.api.rest.v1.chatgpt4 as chatgpt_api
import lib.api.rest.v1.dalle as dalle_api
import lib.api.rest.v1.health as health_api
import lib.app.fastapi.errors as app_errors
import lib.app.fastapi.settings as app_settings
import lib.chatgpt.services as chatgpt_services
import lib.dalle.serveces as dalle_services

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

        logger.info("Initializing chat_models")
        openai_llm = langchain_openai.OpenAI(temperature=0.9, openai_api_key=settings.OPENAI_API_KEY)

        logger.info("Initializing services")
        dalle_service = dalle_services.DalleServece(dalle_llm=openai_llm)
        chatgpt_service = chatgpt_services.ChatGPTServece(chatgpt_llm=openai_llm)

        logger.info("Initializing handlers")
        liveness_probe_handler = health_api.LivenessProbeHandler()
        promt_create_handler = health_api.PromtCreateHandler()
        promt_detail_handler = health_api.PromtDetailHandler()
        dalle_create_handler = dalle_api.DalleCreateHandler(dalle_service=dalle_service)
        chatgpt_create_handler = chatgpt_api.ChatGPT4CreateHandler(chatgpt_service=chatgpt_service)

        logger.info("Creating fastapi application")
        fastapi_app = fastapi.FastAPI()

        logger.info("Initializing routes")
        # ping
        fastapi_app.get("/api/v1/health/liveness", tags=["ping"])(liveness_probe_handler.process)
        fastapi_app.post("/api/v1/promt", tags=["ping"])(promt_create_handler.process)
        fastapi_app.get("/api/v1/promt/{promt_id}", tags=["ping"])(promt_detail_handler.process)

        # OpenAI
        fastapi_app.post("/api/v1/openai/chat", tags=["OpenAI"])(chatgpt_create_handler.process)
        fastapi_app.post("/api/v1/openai/dalle", tags=["OpenAI"])(dalle_create_handler.process)

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
