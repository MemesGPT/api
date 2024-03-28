import typing

import sqlalchemy.ext.asyncio as sqlalchemy_asyncio
import sqlalchemy.orm as sqlalchemy_orm

AsyncEngine = sqlalchemy_asyncio.AsyncEngine
AsyncSession = sqlalchemy_asyncio.AsyncSession
if typing.TYPE_CHECKING:
    AsyncSessionMaker = sqlalchemy_orm.sessionmaker[AsyncSession]  # type: ignore
else:
    AsyncSessionMaker = sqlalchemy_orm.sessionmaker
AsyncSessionContext = typing.AsyncGenerator[AsyncSession, None]

__all__ = [
    "AsyncEngine",
    "AsyncSession",
    "AsyncSessionContext",
    "AsyncSessionMaker",
]
