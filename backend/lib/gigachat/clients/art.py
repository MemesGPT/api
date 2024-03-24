import logging
import typing

import aiohttp

import lib.gigachat.clients.auth as gigachat_auth
import lib.gigachat.config as gigachat_configs
import lib.gigachat.schemes as gigachat_schemes
import lib.gigachat.utils as gigachat_utils

logger = logging.getLogger(__name__)
gigachat_config = gigachat_configs.GigachatConfig()


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
        promt_str = gigachat_config.start_art_promt_template.format(promt_str)
        url = gigachat_config.chat_completions_url
        headers = gigachat_schemes.HeaderFetchImageIdScheme(authorization=f"Bearer {token}").dict(by_alias=True)
        user_message = gigachat_schemes.UserMessageScheme(content=promt_str)
        art_message = gigachat_schemes.ArtMessageScheme(messages=[user_message]).dict()

        async with self._provider.post(url=url, headers=headers, json=art_message, ssl=False) as response:
            result = await response.json()
            if image_id := gigachat_utils.get_image_id_from_response(result):
                return image_id
            raise self.GigachatArtImageNotCreatedError

    async def _fetch_image_bytes_by_id(self, image_id: str, token: str) -> bytes:
        url = gigachat_config.fetch_img_by_id_url.format(image_id)
        headers = gigachat_schemes.HeaderFetchImageScheme(authorization=f"Bearer {token}").dict(by_alias=True)

        async with self._provider.get(url=url, headers=headers, ssl=False) as response:
            return await response.read()


__all__ = [
    "GigachatArtClientProtocol",
    "GigachatArtClient",
]
