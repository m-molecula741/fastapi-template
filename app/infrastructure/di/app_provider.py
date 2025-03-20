"""Модуль для настройки DI контейнера."""

from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.token_service import ITokenService
from app.domain.interfaces.uow import IUOW
from app.infrastructure.config.settings import Settings, get_settings
from app.infrastructure.database.session import get_session
from app.infrastructure.database.uow import UOW
from app.infrastructure.services.token_service import TokenService


class AppProvider(Provider):
    """Провайдер зависимостей приложения."""

    def __init__(self) -> None:
        """Инициализирует провайдер."""
        super().__init__(scope=Scope.APP)

    @provide
    def settings(self) -> Settings:
        """Предоставляет настройки приложения."""
        return get_settings()

    @provide(scope=Scope.REQUEST)
    async def session(self) -> AsyncIterable[AsyncSession]:
        """Предоставляет сессию базы данных."""
        async_session = get_session()
        async for session in async_session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def uow(self, session: AsyncSession) -> IUOW:
        """Предоставляет Unit of Work."""
        return UOW(session)

    @provide
    def token_service(self, settings: Settings) -> ITokenService:
        """Предоставляет сервис для работы с токенами."""
        return TokenService(settings.SECRET_KEY, settings.JWT_ALGORITHM)
