"""Use case для логина пользователя."""

from datetime import datetime, timezone
from app.domain.dto.auth import LoginDTO, TokenDTO
from app.domain.entities.auth import AuthSession
from app.domain.entities.user import User
from app.domain.interfaces.token_service import ITokenService
from app.domain.interfaces.uow import IUOW
from uuid_extensions import uuid7


class LoginUseCase:
    """Use case для логина пользователя."""

    def __init__(self, uow: IUOW, token_service: ITokenService):
        """Инициализирует use case для логина."""
        self.uow = uow
        self.token_service = token_service

    async def execute(self, login_data: LoginDTO) -> TokenDTO:
        """Авторизует пользователя и возвращает токены."""
        async with self.uow:          
            user = await self.uow.users.find_by_email(login_data.email)
            if not user or not user.verify_password(login_data.password):
                raise ValueError("Неверный email или пароль")
            
            access_token = self.token_service.generate_access_token(user.email)
            refresh_token = self.token_service.generate_refresh_token()
            expires_at = self.token_service.get_refresh_token_expires_at()

            auth_session = AuthSession(
                uuid=uuid7(),
                refresh_token=refresh_token,
                expires_at=expires_at,
                user_email=user.email,
                created_at=datetime.now(timezone.utc),
            )
            
            await self.uow.auth_sessions.add(auth_session)
            await self.uow.commit()

            return TokenDTO(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=expires_at
            )
