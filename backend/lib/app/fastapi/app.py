from __future__ import annotations
import asyncio
import logging

import fastapi
import httpx
import langchain.chat_models as ai_chat_models
import langchain_openai
import langserve
import uvicorn

import lib.api.rest.v1.dalle as dalle_api
import lib.api.rest.v1.health as health_api
import lib.api.rest.v1.promt as promt_api
import lib.app.fastapi.errors as app_errors
import lib.app.fastapi.settings as app_settings
import lib.dalle.serveces as dalle_serveces

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
        dalle_llm = langchain_openai.OpenAI(
            temperature=0.9,
            timeout=httpx.Timeout(60.0, read=10.0, write=20.0, connect=10.0),
        )

        openapi_model = ai_chat_models.ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
        )

        logger.info("Initializing services")
        dalle_service = dalle_serveces.DalleServece(dalle_llm=dalle_llm)

        logger.info("Initializing handlers")
        liveness_probe_handler = health_api.LivenessProbeHandler()
        promt_detail_handler = promt_api.PromtDetailHandler()
        promt_create_handler = promt_api.PromtCreateHandler()
        dalle_create_handler = dalle_api.DalleCreateHandler(dalle_service=dalle_service)

        logger.info("Creating fastapi application")
        fastapi_app = fastapi.FastAPI()

        logger.info("Initializing routes")
        # ping
        fastapi_app.get("/api/v1/health/liveness", tags=["ping"])(liveness_probe_handler.process)
        # promt
        fastapi_app.post("/api/v1/promt", tags=["promt"])(promt_create_handler.process)
        fastapi_app.get("/api/v1/promt/{promt_id}", tags=["promt"])(promt_detail_handler.process)
        # dall-e promt
        fastapi_app.post("/api/v1/dalle", tags=["OpenAI Dall-E"])(dalle_create_handler.process)


        logger.info("Initializing langserve routes")

        langserve.add_routes(
            app=fastapi_app,
            runnable=openapi_model,
            path="/openai",
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
