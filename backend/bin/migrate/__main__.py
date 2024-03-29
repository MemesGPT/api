import asyncio
import logging
import os
import sys

import sqlalchemy
import sqlalchemy.ext.asyncio as sqlalchemy_asyncio

import lib.app.fastapi as app
import lib.utils.sqlalchemy as sqlalchemy_utils

logger = logging.getLogger(__name__)


async def run() -> None:
    settings = app.Settings()
    url = sqlalchemy.engine.URL.create(
        drivername="postgresql+asyncpg",
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.PG_MASTER_HOST,
        port=settings.PG_MASTER_PORT,
        database=settings.POSTGRES_DB,
    )
    engine = sqlalchemy_asyncio.create_async_engine(
        url=url,
        echo=settings.is_development,
        pool_size=settings.PG_CONNECTION_POOL_SIZE,
    )

    async with engine.begin() as connection:
        await connection.run_sync(sqlalchemy_utils.Base.metadata.drop_all)
        await connection.run_sync(sqlalchemy_utils.Base.metadata.create_all)


def main() -> None:
    try:
        asyncio.run(run())
        sys.exit(os.EX_OK)
    except SystemExit:
        sys.exit(os.EX_OK)
    except app.AppError:
        sys.exit(os.EX_SOFTWARE)
    except BaseException:
        logger.exception("Unexpected error occurred")
        sys.exit(os.EX_SOFTWARE)


if __name__ == "__main__":
    main()
