from abc import ABC, abstractmethod

from app.domain.interfaces.auth_session_repo import IAuthSessionRepository
from app.domain.interfaces.user_repo import IUserRepository


class IUOW(ABC):
    @abstractmethod
    async def commit(self) -> None:
        """Применяет все изменения."""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """Откатывает все изменения."""
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        """Вход в контекстный менеджер."""
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекстного менеджера."""
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    @property
    def users(self) -> IUserRepository:
        raise NotImplementedError

    @property
    def auth_sessions(self) -> IAuthSessionRepository:
        raise NotImplementedError
