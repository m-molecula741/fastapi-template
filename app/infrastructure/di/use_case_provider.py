"""Провайдеры зависимостей для DI контейнера."""

from uuid import UUID

from dishka import Provider, Scope, provide
from fastapi import Request

from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.logout import LogoutUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.application.use_cases.users.get_current_user import GetCurrentUserUseCase
from app.application.use_cases.users.register import RegisterUserUseCase
from app.domain.interfaces.token_service import ITokenService
from app.domain.interfaces.uow import IUOW


class UseCaseProvider(Provider):
    """Провайдер для Use Cases."""

    def __init__(self) -> None:
        """Инициализирует провайдер."""
        super().__init__(scope=Scope.REQUEST)

    @provide
    async def register_user_usecase(self, uow: IUOW) -> RegisterUserUseCase:
        """Предоставляет use case для регистрации пользователей."""
        return RegisterUserUseCase(uow)

    @provide
    async def login_usecase(
        self, uow: IUOW, token_service: ITokenService
    ) -> LoginUseCase:
        """Предоставляет use case для входа пользователей."""
        return LoginUseCase(uow, token_service)

    @provide
    async def logout_usecase(self, uow: IUOW, request: Request) -> LogoutUseCase:
        """Предоставляет use case для выхода пользователей."""
        refresh_token = UUID(request.cookies.get("refresh_token"))
        return LogoutUseCase(uow, refresh_token)

    @provide
    async def refresh_token_usecase(
        self, uow: IUOW, token_service: ITokenService, request: Request
    ) -> RefreshTokenUseCase:
        """Предоставляет use case для обновления токена."""
        refresh_token = UUID(request.cookies.get("refresh_token"))
        return RefreshTokenUseCase(uow, token_service, refresh_token)

    @provide
    async def get_current_user_usecase(
        self, uow: IUOW, token_service: ITokenService, request: Request
    ) -> GetCurrentUserUseCase:
        """Предоставляет use case для получения текущего пользователя."""
        access_token = request.cookies.get("access_token")
        return GetCurrentUserUseCase(uow, token_service, access_token)
