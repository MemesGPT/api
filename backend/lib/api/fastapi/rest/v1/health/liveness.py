import json
import logging

import fastapi

import lib.utils.fastapi as fastapi_utils

logger = logging.getLogger(__name__)


class LivenessProbeHandler(fastapi_utils.HandlerProtocol):
    async def process(self, request: fastapi.Request) -> fastapi.Response:
        return fastapi.Response(
            status_code=200,
            content=json.dumps({"status": "healthy"}),
        )


__all__ = [
    "LivenessProbeHandler",
]
