import typing

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI


class ChatGPTServeceProtocol(typing.Protocol):
    async def create(self, promt_str: str) -> str:
        ...


class ChatGPTServece(ChatGPTServeceProtocol):
    def __init__(self, chatgpt_llm: OpenAI) -> None:
        self._chatgpt_llm = chatgpt_llm

    async def create(self, promt_str: str) -> str:
        template = """Вопрос: {question}

        Ответ: Давайте подумаем шаг за шагом."""

        prompt = PromptTemplate.from_template(template)
        llm_chain = LLMChain(prompt=prompt, llm=self._chatgpt_llm)

        return llm_chain.run(promt_str)


__all__ = [
    "ChatGPTServece",
    "ChatGPTServeceProtocol",
]
