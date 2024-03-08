import typing

import faker

import lib.api.rest.v1.promt.schemes as promt_schemes

fake = faker.Faker()
faker.Faker.seed(1234)


class PromtDetailHandlerProtocol(typing.Protocol):
    async def process(self) -> promt_schemes.PromtScheme:
        ...


class PromtDetailHandler(PromtDetailHandlerProtocol):
    async def process(self) -> promt_schemes.PromtScheme:
        return promt_schemes.PromtScheme(
            id=fake.uuid4(),
            text=fake.sentence(nb_words=10),
        )


__all__ = [
    "PromtDetailHandlerProtocol",
    "PromtDetailHandler",
]
