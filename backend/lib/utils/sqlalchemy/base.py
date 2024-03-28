import typing

import sqlalchemy.inspection as sqlalchemy_inspection
import sqlalchemy.orm as sqlalchemy_orm


def implement_as_dict(model: typing.Type[typing.Any]) -> None:  # noqa: FA100
    column_names: list[str] = [column.key for column in sqlalchemy_inspection.inspect(model).columns]

    def as_dict(self) -> dict[str, typing.Any]:  # noqa: ANN001
        return {column: getattr(self, column) for column in column_names}

    model.as_dict = as_dict


class CustomBaseMetaclass(sqlalchemy_orm.DeclarativeMeta):
    def __init__(cls, classname: typing.Any, bases: typing.Any, dict_: typing.Any, **kw: typing.Any) -> None:  # noqa: ANN401, N805
        super().__init__(classname, bases, dict_, **kw)
        if not bases:
            return
        implement_as_dict(cls)


mapper_registry = sqlalchemy_orm.registry()


class Base(metaclass=CustomBaseMetaclass):
    __abstract__ = True

    registry = mapper_registry
    metadata = mapper_registry.metadata

    __init__ = mapper_registry.constructor

    def as_dict(self) -> dict[str, typing.Any]:  # type: ignore
        # implemented in implement_as_dict during runtime-bind in CustomBaseMetaclass
        pass


__all__ = [
    "Base",
]
