import logging
import typing

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_openai import OpenAI

logger = logging.getLogger(__name__)


class DalleServiceProtocol(typing.Protocol):
    async def create(self, promt_str: str) -> str:
        ...


class DalleServece(DalleServiceProtocol):
    def __init__(self, dalle_llm: OpenAI) -> None:
        self._dalle_llm = dalle_llm

    async def create(self, promt_str: str) -> str:
        prompt = PromptTemplate(
            input_variables=["image_desc"],
            template="{image_desc}",
        )
        chain = LLMChain(llm=self._dalle_llm, prompt=prompt)
        return DallEAPIWrapper().run(chain.run(promt_str))


__all__ = [
    "DalleServece",
    "DalleServiceProtocol",
]
