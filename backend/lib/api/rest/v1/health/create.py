import typing

import faker

import lib.api.rest.v1.promt.schemes as promt_schemes

fake = faker.Faker()
faker.Faker.seed(1234)


class PromtCreateHandlerProtocol(typing.Protocol):
    class NotCreatedError(Exception):
        ...

    async def process(
              self,
              promt: promt_schemes.PromtWithoutId,
    ) -> promt_schemes.PromtScheme:
        ...


class PromtCreateHandler(PromtCreateHandlerProtocol):
    async def process(
              self,
              promt_in: promt_schemes.PromtWithoutId,
    ) -> promt_schemes.PromtScheme:
        return promt_schemes.PromtScheme(
            id=fake.uuid4(),
            text=promt_in.text,
        )


__all__ = [
    "PromtCreateHandlerProtocol",
    "PromtCreateHandler",
]
