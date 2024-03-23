import typing
import uuid

import pydantic


class GigachatArtPromtScheme(pydantic.BaseModel):
    text: str


class GigachatArtImgScheme(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(default=uuid.uuid4())
    image: typing.Any


__all__ = [
    "GigachatArtPromtScheme",
    "GigachatArtImgScheme",
]
