"""Модуль для работы с сессией SQLAlchemy."""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.infrastructure.config.settings import get_settings
from app.infrastructure.logging.logger import logger


settings = get_settings()


DATABASE_URL = settings.db_url


engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Отключаем вывод SQL запросов независимо от настроек
    future=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Получает сессию базы данных."""
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()


async def create_tables():
    """Создает все таблицы в базе данных."""
    from app.infrastructure.database.models.base import Base
    
    logger.info("Начало создания таблиц в базе данных")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Таблицы успешно созданы") 