import uuid

import pydantic


class DallePromtScheme(pydantic.BaseModel):
    text: str


class ImageScheme(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(default=uuid.uuid4())
    image_url: str


__all__ = [
    "DallePromtScheme",
    "ImageScheme",
]
