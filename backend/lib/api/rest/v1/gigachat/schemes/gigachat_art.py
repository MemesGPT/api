import pydantic


class GigachatArtPromtScheme(pydantic.BaseModel):
    text: str


__all__ = [
    "GigachatArtPromtScheme",
]
