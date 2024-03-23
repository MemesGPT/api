import ssl
import typing
import uuid

import aiohttp


class GigachatAuthClientProtocol(typing.Protocol):
    async def fetch_token(self) -> str:
        ...


class GigachatAuthClient(GigachatAuthClientProtocol):
    def __init__(self, provider: aiohttp.ClientSession, token: str) -> None:
        self._provider = provider
        self._token = token

    async def fetch_token(self) -> str:
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        payload = "scope=GIGACHAT_API_PERS"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": f"Basic {self._token}",
        }
        async with self._provider.post(url=url, data=payload, headers=headers, ssl=self._ssl_context()) as response:
            result = await response.json()
            return result.get("access_token")

    @staticmethod
    def _ssl_context() -> ssl.SSLContext:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context


__all__ = [
    "GigachatAuthClient",
    "GigachatAuthClientProtocol",
]
