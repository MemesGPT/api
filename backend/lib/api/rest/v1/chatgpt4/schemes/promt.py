import pydantic


class PromtScheme(pydantic.BaseModel):
    text: str


__all__ = [
    "PromtScheme",
]
