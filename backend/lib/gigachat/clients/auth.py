import typing
import uuid

import aiohttp

import lib.gigachat.config as gigachat_configs
import lib.gigachat.schemes as gigachat_schemes

gigachat_config = gigachat_configs.GigachatConfig()


class GigachatAuthClientProtocol(typing.Protocol):
    async def fetch_token(self) -> str:
        ...


class GigachatAuthClient(GigachatAuthClientProtocol):
    def __init__(self, provider: aiohttp.ClientSession, token: str) -> None:
        self._provider = provider
        self._token = token

    async def fetch_token(self) -> str:
        url = gigachat_config.auth_url
        payload = "scope=GIGACHAT_API_PERS"
        headers = gigachat_schemes.HeaderFetchTokenScheme(
            rquid=uuid.uuid4(),
            authorization=f"Basic {self._token}",
        ).dict(by_alias=True)
        async with self._provider.post(url=url, data=payload, headers=headers, ssl=False) as response:
            result = await response.json()
            return result.get("access_token")


__all__ = [
    "GigachatAuthClient",
    "GigachatAuthClientProtocol",
]
