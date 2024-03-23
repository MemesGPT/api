import typing

import lib.gigachat.clients as gigachat_clients


class GigachatArtServiceProtocol(typing.Protocol):
    async def create(self, promt_str: str) -> str:
        ...


class GigachatArtService(GigachatArtServiceProtocol):
    def __init__(self, gigachat_client: gigachat_clients.GigachatArtClientProtocol) -> None:
        self._gigachat_client = gigachat_client

    async def create(self, promt_str: str) -> str:
        return await self._gigachat_client.generate_image(promt_str=promt_str)


__all__ = [
    "GigachatArtService",
    "GigachatArtServiceProtocol",
]
