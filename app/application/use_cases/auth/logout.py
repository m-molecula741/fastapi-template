"""Use Case для выхода пользователя из системы."""

from uuid import UUID

from app.domain.exceptions import RefreshTokenException
from app.domain.interfaces.uow import IUOW


class LogoutUseCase:
    """Use Case для выхода пользователя из системы."""

    def __init__(self, uow: IUOW, refresh_token: UUID):
        self.uow = uow
        self.refresh_token = refresh_token

    async def execute(self) -> None:
        """Выполняет выход пользователя из системы."""
        async with self.uow:
            auth_session = await self.uow.auth_sessions.find_by_refresh_token(
                self.refresh_token
            )
            if not auth_session:
                raise RefreshTokenException(message="Сессия не найдена")

            await self.uow.auth_sessions.delete_by_refresh_token(self.refresh_token)
