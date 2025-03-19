"""Зависимости для FastAPI."""
from typing import Annotated
from fastapi import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.logout import LogoutUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.application.use_cases.users.get_current_user import GetCurrentUserUseCase
from app.application.use_cases.users.register import RegisterUserUseCase
from app.domain.dto.user import UserDTO
from app.domain.exceptions import AuthenticationException
from app.domain.interfaces.token_service import ITokenService
from app.domain.interfaces.uow import IUOW
from app.infrastructure.database.session import get_session
from app.infrastructure.database.uow import UOW
from app.infrastructure.services.token_service import TokenService
from app.infrastructure.config.settings import get_settings
from app.infrastructure.logging.logger import log_info, log_warning


settings = get_settings()

async def get_uow(session: AsyncSession = Depends(get_session)) -> IUOW:
    """Предоставляет Transaction Manager."""
    return UOW(session)


async def get_token_service() -> ITokenService:
    """Предоставляет сервис для работы с токенами."""
    return TokenService(settings.SECRET_KEY, settings.JWT_ALGORITHM)


async def get_register_usecase(
    uow: IUOW = Depends(get_uow)
) -> RegisterUserUseCase:
    """Предоставляет use case для регистрации пользователя."""
    return RegisterUserUseCase(uow)


async def get_login_usecase(
    uow: IUOW = Depends(get_uow),
    token_service: ITokenService = Depends(get_token_service)
) -> LoginUseCase:
    """Предоставляет use case для авторизации пользователя."""
    return LoginUseCase(uow, token_service)


async def get_current_user_usecase(
    uow: IUOW = Depends(get_uow),
    token_service: ITokenService = Depends(get_token_service)
) -> GetCurrentUserUseCase:
    """Предоставляет use case для получения текущего пользователя."""
    return GetCurrentUserUseCase(uow, token_service)


async def get_acces_token_from_cookie(
    access_token: str | None = Cookie(default=None, alias="access_token"),
) -> str:
    """Извлекает токен из куки."""
    if not access_token:
        log_warning("Запрос без токена доступа")
        raise AuthenticationException(message="Токен не предоставлен")
    
    log_info("Получен токен доступа из cookie")
    return access_token


async def get_current_user(
    access_token: Annotated[str, Depends(get_acces_token_from_cookie)],
    usecase: Annotated[GetCurrentUserUseCase, Depends(get_current_user_usecase)],
) -> UserDTO:
    """Зависимость для получения текущего пользователя."""
    try:
        user = await usecase.execute(token=access_token)
        log_info("Пользователь успешно аутентифицирован", email=user.email)
        return user
    except Exception as e:
        log_warning("Ошибка аутентификации", error=str(e))
        raise AuthenticationException(message=str(e))


async def get_refresh_token_from_cookie(
    refresh_token: str | None = Cookie(default=None, alias="refresh_token"),
) -> str:
    """Извлекает refresh token из куки."""
    if not refresh_token:
        log_warning("Запрос без refresh-токена")
        raise AuthenticationException(message="Refresh-токен не предоставлен")
    
    log_info("Получен refresh-токен из cookie")
    return refresh_token


async def get_refresh_token_usecase(
    uow: IUOW = Depends(get_uow),
    token_service: ITokenService = Depends(get_token_service)
) -> RefreshTokenUseCase:
    """Предоставляет use case для обновления refresh token."""
    return RefreshTokenUseCase(uow, token_service)


async def get_logout_usecase(
    uow: IUOW = Depends(get_uow),
) -> LogoutUseCase:
    """Предоставляет use case для выхода пользователя из системы."""
    return LogoutUseCase(uow)
