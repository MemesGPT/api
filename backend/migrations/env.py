import logging
import logging.config as logging_config
import pathlib
import sys
import urllib
from collections.abc import Iterable

from alembic import context
from alembic.environment import MigrationContext
from alembic.operations import MigrationScript
from sqlalchemy import engine_from_config, pool

base_dir = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(base_dir))

import lib.app.fastapi.settings as app_settings
from lib.utils.sqlalchemy import mapper_registry

settings: app_settings.Settings = app_settings.Settings()
logger = logging.getLogger("alembic.env")


def get_sqlalchemy_url() -> str:
    user = settings.POSTGRES_USER
    password = urllib.parse.quote_plus(settings.POSTGRES_PASSWORD).replace("%", "%%")
    server = settings.PG_MASTER_HOST
    port = settings.PG_MASTER_PORT
    db = settings.POSTGRES_DB
    return f"postgresql+psycopg2://{user}:{password}@{server}:{port}/{db}"


config = context.config
if config.config_file_name is not None:
    logging_config.fileConfig(config.config_file_name)
config.set_main_option("sqlalchemy.url", get_sqlalchemy_url())
target_metadata = mapper_registry.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    def process_revision_directives(
        context: MigrationContext,
        revision: str | Iterable[str | None] | Iterable[str],
        directives: list[MigrationScript],
    ) -> None:
        assert config.cmd_opts is not None
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            assert script.upgrade_ops is not None
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes in schema detected.")

    configuration = config.get_section(config.config_ini_section)
    if configuration is None:
        raise RuntimeError
    configuration["sqlalchemy.url"] = config.get_main_option("sqlalchemy.url") or ""

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
