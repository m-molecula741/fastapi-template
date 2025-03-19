"""Интерфейс для репозитория авторизационных сессий."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import UUID

from app.domain.entities.auth import AuthSession


class IAuthSessionRepository(ABC):
    """Интерфейс для репозитория авторизационных сессий."""

    @abstractmethod
    async def add(self, auth_session: AuthSession) -> None:
        """Добавляет новую авторизационную сессию."""
        pass

    @abstractmethod
    async def find_by_refresh_token(self, refresh_token: UUID) -> Optional[AuthSession]:
        """Находит авторизационную сессию по refresh token."""
        pass

    @abstractmethod
    async def update_refresh_token(
        self, uuid: UUID, refresh_token: UUID, expires_at: datetime
    ) -> None:
        """Обновляет refresh token."""
        pass

    @abstractmethod
    async def delete_by_refresh_token(self, refresh_token: UUID) -> None:
        """Удаляет авторизационную сессию по refresh token."""
        pass
