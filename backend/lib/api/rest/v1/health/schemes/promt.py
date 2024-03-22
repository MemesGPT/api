import uuid

import pydantic


class PromtWithoutId(pydantic.BaseModel):
    text: str


class PromtScheme(PromtWithoutId):
    id: uuid.UUID


__all__ = [
    "PromtScheme",
    "PromtWithoutId",
]
