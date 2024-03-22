import typing
import uuid

import faker

import lib.api.rest.v1.health.schemes as promt_schemes

fake = faker.Faker()
faker.Faker.seed(1234)


class PromtDetailHandlerProtocol(typing.Protocol):
    async def process(self, promt_id: uuid.UUID) -> promt_schemes.PromtScheme:
        ...


class PromtDetailHandler(PromtDetailHandlerProtocol):
    async def process(self, promt_id: uuid.UUID) -> promt_schemes.PromtScheme:
        return promt_schemes.PromtScheme(
            id=promt_id,
            text=fake.sentence(nb_words=10),
        )


__all__ = [
    "PromtDetailHandlerProtocol",
    "PromtDetailHandler",
]
