"""Механизм реализации миграций"""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine.base import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from app.infrastructure.config.settings import get_settings
from app.infrastructure.database.models.base import Base

# Получаем экземпляр настроек
settings = get_settings()

config = context.config

fileConfig(config.config_file_name)

target_metadata = Base.metadata

config.set_main_option("sqlalchemy.url", settings.db_url)


def run_migrations_offline() -> None:
    """Запуск миграции в оффлайн режиме"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Запуск миграции

    Args:
        connection (Connection): [Сессия с БД]
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        include_schemas=True,
        version_table_schema=target_metadata.schema,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запускаем миграцию в онлайн режиме"""
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )
    connectable = AsyncEngine(engine)  # error_type: ignore

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)  # error_type: ignore


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
