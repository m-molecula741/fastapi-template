"""SQLAlchemy реализация репозитория авторизационных сессий."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.auth import AuthSession
from app.domain.interfaces.auth_session_repo import IAuthSessionRepository
from app.infrastructure.database.models.auth import AuthSessionModel

class AuthSessionRepository(IAuthSessionRepository):
    """SQLAlchemy реализация репозитория авторизационных сессий."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, auth_session: AuthSession) -> None:
        """Добавляет новую авторизационную сессию."""
        await self.session.execute(
            insert(AuthSessionModel).values(**auth_session.to_dict())
        )

    async def find_by_refresh_token(self, refresh_token: UUID) -> Optional[AuthSession]:
        """Находит авторизационную сессию по refresh token."""
        stmt = select(AuthSessionModel).where(AuthSessionModel.refresh_token == refresh_token)
        result = await self.session.execute(stmt)
        auth_session_model = result.scalar_one_or_none()

        if auth_session_model:
            return AuthSession(
                uuid=auth_session_model.uuid,
                refresh_token=auth_session_model.refresh_token,
                expires_at=auth_session_model.expires_at,
                user_email=auth_session_model.user_email
            )
        return None

    async def update_refresh_token(
        self, uuid: UUID, refresh_token: UUID, expires_at: datetime
    ) -> None:
        """Обновляет refresh token."""
        await self.session.execute(
            update(AuthSessionModel).where(
                AuthSessionModel.uuid == uuid
            ).values(refresh_token=refresh_token, expires_at=expires_at)
        )

    async def delete_by_refresh_token(self, refresh_token: UUID) -> None:
        """Удаляет авторизационную сессию по refresh token."""
        await self.session.execute(
            delete(AuthSessionModel).where(AuthSessionModel.refresh_token == refresh_token)
        )
