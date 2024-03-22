import uuid

import pydantic


class AnswerWithoutId(pydantic.BaseModel):
    text: str


class AnswerScheme(AnswerWithoutId):
    id: uuid.UUID


__all__ = [
    "AnswerScheme",
    "AnswerWithoutId",
]
