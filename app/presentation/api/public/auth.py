"""API для работы с авторизацией."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.domain.exceptions import AuthenticationException
from app.infrastructure.config.settings import get_settings
from app.infrastructure.logging.logger import log_error, log_info
from app.presentation.api.dependencies import (
    get_login_usecase,
    get_refresh_token_from_cookie,
    get_refresh_token_usecase,
)
from app.presentation.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()
settings = get_settings()


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    login_data: LoginRequest,
    login_usecase: Annotated[LoginUseCase, Depends(get_login_usecase)],
    response: Response,
):
    """Эндпоинт для авторизации пользователя."""
    log_info("Получен запрос на авторизацию", email=login_data.email)

    try:
        login_dto = login_data.to_dto()
        tokens = await login_usecase.execute(login_dto)

        # Устанавливаем куки для токенов
        response.set_cookie(
            key="access_token",
            value=tokens.access_token,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=settings.ENVIRONMENT == "production",
            samesite="lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            httponly=True,
            secure=settings.ENVIRONMENT == "production",
            samesite="lax",
        )

        log_info("Пользователь успешно авторизован", email=login_data.email)
        return TokenResponse.from_dto(tokens)
    except Exception as e:
        log_error("Ошибка при авторизации", error=e, email=login_data.email)
        raise AuthenticationException(message=str(e)) from e


@router.patch("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh(
    refresh_token: Annotated[str, Depends(get_refresh_token_from_cookie)],
    refresh_token_usecase: Annotated[
        RefreshTokenUseCase, Depends(get_refresh_token_usecase)
    ],
    response: Response,
):
    """Эндпоинт для обновления refresh token."""
    log_info("Получен запрос на обновление токена")

    try:
        tokens = await refresh_token_usecase.execute(refresh_token)

        # Устанавливаем куки для новых токенов
        response.set_cookie(
            key="access_token",
            value=tokens.access_token,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=settings.ENVIRONMENT == "production",
            samesite="lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            httponly=True,
            secure=settings.ENVIRONMENT == "production",
            samesite="lax",
        )

        log_info("Токены успешно обновлены")
        return TokenResponse.from_dto(tokens)
    except Exception as e:
        log_error("Ошибка при обновлении токенов", error=e)
        raise AuthenticationException(message=str(e)) from e
