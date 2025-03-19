"""Use Case для выхода пользователя из системы."""
from uuid import UUID
from app.domain.interfaces.uow import IUOW
from app.domain.exceptions import RefreshTokenException

class LogoutUseCase:
    """Use Case для выхода пользователя из системы."""

    def __init__(self, uow: IUOW):
        self.uow = uow

    async def execute(self, refresh_token: UUID) -> None:
        """Выполняет выход пользователя из системы."""
        async with self.uow:
            auth_session = await self.uow.auth_sessions.find_by_refresh_token(refresh_token)
            if not auth_session:
                raise RefreshTokenException(message="Сессия не найдена")

            await self.uow.auth_sessions.delete_by_refresh_token(refresh_token)
