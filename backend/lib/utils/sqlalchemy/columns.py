import typing

import sqlalchemy
import sqlalchemy.orm as sqlalchemy_orm
import sqlalchemy.sql.type_api as sqlalchemy_type_api

T = typing.TypeVar("T")
_TypeEngine = typing.TypeVar("_TypeEngine", bound=sqlalchemy_type_api.TypeEngine[typing.Any])


def mapped_column(
    *,
    mapped_type: type[T],
    column_name: str,
    column_type: _TypeEngine | type[_TypeEngine],
    **kwargs: typing.Any,  # noqa: ANN401
) -> sqlalchemy_orm.Mapped[T]:
    column = sqlalchemy.Column(name=column_name, type_=column_type, **kwargs)
    return typing.cast(sqlalchemy_orm.Mapped[mapped_type], column)  # type: ignore


__all__ = [
    "mapped_column",
]
