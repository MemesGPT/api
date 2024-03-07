import typing


class AppError(Exception):
    def __init__(self, message: str, *args: typing.Any) -> None:  # noqa: ANN401
        super().__init__(*args)
        self.message = message


class DisposeError(AppError):
    pass


class StartServerError(AppError):
    pass


__all__ = [
    "AppError",
    "DisposeError",
    "StartServerError",
]
