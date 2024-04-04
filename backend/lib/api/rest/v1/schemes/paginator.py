import fastapi
import pydantic


class SearchEnginePaginate:
    def __init__(
        self,
        size: pydantic.PositiveInt = fastapi.Query(default=50, alias="page[size]"),
        number: pydantic.PositiveInt = fastapi.Query(default=1, alias="page[number]"),
    ) -> None:
        self.size = size
        self.number = number


class Paginator(pydantic.BaseModel):
    total_pages: pydantic.NonNegativeInt
    total_items: pydantic.NonNegativeInt
    number: pydantic.PositiveInt
    size: pydantic.PositiveInt


__all__ = [
    "Paginator",
    "SearchEnginePaginate",
]
