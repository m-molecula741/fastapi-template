"""Интерфейс для сервиса работы с токенами."""

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID


class ITokenService(ABC):
    """Интерфейс для сервиса работы с токенами."""

    @abstractmethod
    def generate_access_token(self, email: str) -> str:
        """Генерирует access token."""
        pass

    @abstractmethod
    def decode_access_token(self, token: str) -> dict:
        """Декодирует access token."""
        pass

    @abstractmethod
    def generate_refresh_token(self) -> UUID:
        """Генерирует refresh token."""
        pass

    @abstractmethod
    def get_refresh_token_expires_at(self) -> datetime:
        """Возвращает срок действия refresh token."""
        pass
