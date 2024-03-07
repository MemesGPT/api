import asyncio
import logging
import os
import sys

import lib.app.fastapi as app

logger = logging.getLogger(__name__)


async def run() -> None:
    settings = app.Settings()
    application = app.Application.from_settings(settings)

    try:
        await application.start()
    finally:
        await application.dispose()


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
