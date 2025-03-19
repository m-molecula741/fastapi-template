"""Use Case для обновления токенов."""

from datetime import datetime, timezone
from uuid import UUID
from app.domain.dto.auth import TokenDTO
from app.domain.exceptions import AuthenticationException, RefreshTokenException
from app.domain.interfaces.token_service import ITokenService
from app.domain.interfaces.uow import IUOW


class RefreshTokenUseCase:
    """Use Case для обновления токенов."""

    def __init__(
        self,
        uow: IUOW,
        token_service: ITokenService,
    ):
        self.uow = uow
        self.token_service = token_service

    async def execute(self, refresh_token: UUID) -> TokenDTO:
        """Обновляет access-токен и refresh-токен."""

        async with self.uow:
            auth_session = await self.uow.auth_sessions.find_by_refresh_token(refresh_token)
            if not auth_session:
                raise RefreshTokenException(message="Недействительный refresh token")

            if auth_session.expires_at < datetime.now(timezone.utc):
                await self.uow.auth_sessions.remove(auth_session.uuid)
                raise RefreshTokenException(message="Срок действия refresh token истек")

            user = await self.uow.users.find_by_email(auth_session.user_email)
            if not user:
                raise AuthenticationException(message="Пользователь не найден")

            access_token = self.token_service.generate_access_token(user.email)
            new_refresh_token = self.token_service.generate_refresh_token()
            refresh_token_expires_at = self.token_service.get_refresh_token_expires_at()

            # Обновляем refresh токен в текущей сессии
            await self.uow.auth_sessions.update_refresh_token(
                auth_session.uuid, 
                new_refresh_token, 
                refresh_token_expires_at
            )
            
            return TokenDTO(
                access_token=access_token,
                refresh_token=new_refresh_token,
                expires_at=refresh_token_expires_at,
            )
