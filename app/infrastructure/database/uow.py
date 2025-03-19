from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.interfaces.uow import IUOW
from app.infrastructure.database.repositories.auth_session_repo import AuthSessionRepository
from app.infrastructure.database.repositories.user_repo import UserRepository


class UOW(IUOW):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        """Фиксирует изменения в базе данных."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Откатывает изменения."""
        await self.session.rollback()

    async def __aenter__(self):
        """Вход в контекстный менеджер."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекстного менеджера."""
        if exc_type is not None:
            print("rollback")
            await self.rollback()
            await self.session.close()
        else:
            print("commit")
            await self.commit()
            await self.session.close()

    @property
    def users(self) -> UserRepository:
        """Доступ к репозиторию юзера"""
        return UserRepository(session=self.session)

    @property
    def auth_sessions(self) -> AuthSessionRepository:
        """Доступ к репозиторию авторизационных сессий"""
        return AuthSessionRepository(session=self.session)
