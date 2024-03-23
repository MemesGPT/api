import logging
import ssl
import typing

import aiohttp

import lib.gigachat.clients.auth as gigachat_auth
import lib.gigachat.utils as gigachat_utils

logger = logging.getLogger(__name__)


class GigachatArtClientProtocol(typing.Protocol):
    class GigachatArtImageNotCreatedError(Exception):
        ...

    async def generate_image(self, promt_str: str) -> bytes:
        ...


class GigachatArtClient(GigachatArtClientProtocol):
    def __init__(
              self,
              provider: aiohttp.ClientSession,
              auth_client: gigachat_auth.GigachatAuthClientProtocol,
    ) -> None:
        self._provider = provider
        self._auth_client = auth_client

    async def generate_image(self, promt_str: str) -> bytes:
        token = await self._auth_client.fetch_token()
        image_id = await self._fetch_image_id_by_promt(promt_str, token)
        return await self._fetch_image_bytes_by_id(image_id, token)

    async def _fetch_image_id_by_promt(self, promt_str: str, token: str) -> str:
        promt_str = f"Нарисуй {promt_str}"
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + token,
        }
        data = {
            "model": "GigaChat",
            "messages": [
                {
                    "role": "user",
                    "content": promt_str,
                },
            ],
            "temperature": 1,
            "top_p": 0.1,
            "n": 1,
            "stream": False,
            "max_tokens": 512,
            "repetition_penalty": 1,
            "update_interval": 0,
        }
        async with self._provider.post(url=url, headers=headers, json=data, ssl=self._ssl_context()) as response:
            result = await response.json()
            if image_id := gigachat_utils.get_image_id_from_response(result):
                return image_id
            raise self.GigachatArtImageNotCreatedError

    async def _fetch_image_bytes_by_id(self, image_id: str, token: str) -> bytes:
        url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{image_id}/content"
        headers = {
            "Accept": "application/jpg",
            "Authorization": "Bearer " + token,
        }
        async with self._provider.get(url=url, headers=headers, ssl=self._ssl_context()) as response:
            return await response.read()

    @staticmethod
    def _ssl_context() -> ssl.SSLContext:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context


__all__ = [
    "GigachatArtClientProtocol",
    "GigachatArtClient",
]
