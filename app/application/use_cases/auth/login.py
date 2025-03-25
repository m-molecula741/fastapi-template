"""Use case для логина пользователя."""

from datetime import UTC, datetime

from uuid_extensions import uuid7

from app.domain.entities.auth import AuthSession, Token
from app.domain.exceptions import AuthenticationException
from app.domain.interfaces.token_service import ITokenService
from app.domain.interfaces.uow import IUOW


class LoginUseCase:
    """Use case для логина пользователя."""

    def __init__(self, uow: IUOW, token_service: ITokenService):
        """Инициализирует use case для логина."""
        self.uow = uow
        self.token_service = token_service

    async def execute(self, email: str, password: str) -> Token:
        """Авторизует пользователя и возвращает токены."""
        async with self.uow:
            user = await self.uow.users.find_by_email(email)
            if not user or not user.verify_password(password):
                raise AuthenticationException(message="Неверный email или пароль")

            access_token = self.token_service.generate_access_token(user.email)
            refresh_token = self.token_service.generate_refresh_token()
            expires_at = self.token_service.get_refresh_token_expires_at()

            auth_session = AuthSession(
                uuid=uuid7(),
                refresh_token=refresh_token,
                expires_at=expires_at,
                user_email=user.email,
                created_at=datetime.now(UTC),
            )

            await self.uow.auth_sessions.add(auth_session)

            return Token(
                access_token=access_token,
                refresh_token=refresh_token,
            )
