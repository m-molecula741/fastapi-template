"""Модуль с функциями для создания репозиториев."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.user_repo import IUserRepository

# Явный реэкспорт
from app.infrastructure.database.repositories.user_repo import (
    UserRepository as UserRepository,
)


def get_user_repository(session: AsyncSession) -> IUserRepository:
    """Создает и возвращает репозиторий пользователей.

    Args:
        session: Асинхронная сессия SQLAlchemy

    Returns:
        Репозиторий пользователей
    """
    return UserRepository(session)


# Здесь можно добавить другие функции для получения других репозиториев
# например:
# def get_product_repository(session: AsyncSession) -> ProductRepository:
#     return ProductRepository(session)
