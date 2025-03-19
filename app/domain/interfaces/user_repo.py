"""Интерфейс репозитория пользователей."""

from abc import ABC, abstractmethod

from app.domain.entities.user import User


class IUserRepository(ABC):
    """Интерфейс репозитория для работы с пользователями."""

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        """Ищет пользователя по email."""
        pass

    @abstractmethod
    async def create_user(self, user: User) -> str:
        """Создает нового пользователя."""
        pass
