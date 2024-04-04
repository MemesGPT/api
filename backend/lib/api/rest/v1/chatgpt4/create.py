import typing

import lib.api.rest.v1.chatgpt4.schemes as chatgpt4_schemes
import lib.chatgpt.services as chatgpt_serveces


class ChatGPT4CreateHandlerProtocol(typing.Protocol):
    class NotCreatedError(Exception):
        ...

    async def process(self, promt: chatgpt4_schemes.PromtScheme) -> chatgpt4_schemes.PromtScheme:
        ...


class ChatGPT4CreateHandler(ChatGPT4CreateHandlerProtocol):
    def __init__(self, chatgpt_service: chatgpt_serveces.ChatGPTServeceProtocol) -> None:
        self._chatgpt_service = chatgpt_service

    async def process(self, promt: chatgpt4_schemes.PromtScheme) -> chatgpt4_schemes.PromtScheme:
        answer_str = await self._chatgpt_service.create(promt_str=promt.text)
        return chatgpt4_schemes.PromtScheme(text=answer_str)


__all__ = [
    "ChatGPT4CreateHandlerProtocol",
    "ChatGPT4CreateHandler",
]
