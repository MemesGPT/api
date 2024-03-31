import pydantic


class Paginator(pydantic.BaseModel):
    total_pages: pydantic.NonNegativeInt
    total_items: pydantic.NonNegativeInt
    number: pydantic.PositiveInt
    size: pydantic.PositiveInt


__all__ = [
    "Paginator",
]
