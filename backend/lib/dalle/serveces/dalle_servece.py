import typing

import langchain.chains as langchain_chains
import langchain.prompts as langchain_prompts
import langchain_community.utilities.dalle_image_generator as dalle_image_generators
import langchain_openai


class DalleServiceProtocol(typing.Protocol):
    async def create(self, promt_in: str) -> str:
        ...


class DalleServece(DalleServiceProtocol):
    def __init__(self, dalle_llm: langchain_openai.OpenAI) -> None:
        self._dalle_llm = dalle_llm

    async def create(self, promt_in: str) -> str:
        prompt = langchain_prompts.PromptTemplate.from_template(
            "Draw a picture that matches this description: {image_desc}.",
        )
        chain = langchain_chains.LLMChain(llm=self._dalle_llm, prompt=prompt)
        return dalle_image_generators.DallEAPIWrapper().run(chain.run(promt_in))


__all__ = [
    "DalleServece",
    "DalleServiceProtocol",
]
