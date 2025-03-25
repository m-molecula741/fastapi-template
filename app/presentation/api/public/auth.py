"""API для работы с авторизацией."""

from dataclasses import asdict

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Response, status

from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.domain.exceptions import AuthenticationException
from app.infrastructure.config.settings import Settings
from app.infrastructure.logging.logger import log_error, log_info
from app.presentation.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
@inject
async def login(
    login_data: LoginRequest,
    response: Response,
    login_usecase: FromDishka[LoginUseCase],
    settings: FromDishka[Settings],
) -> TokenResponse:
    """Эндпоинт для авторизации пользователя."""
    log_info("Получен запрос на авторизацию", email=login_data.email)

    try:
        tokens = await login_usecase.execute(
            email=login_data.email, password=login_data.password
        )

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
            value=str(tokens.refresh_token),
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            httponly=True,
            secure=settings.ENVIRONMENT == "production",
            samesite="lax",
        )

        log_info("Пользователь успешно авторизован", email=login_data.email)
        return TokenResponse(**asdict(tokens))
    except Exception as e:
        log_error("Ошибка при авторизации", error=e, email=login_data.email)
        raise AuthenticationException(message=str(e)) from e


@router.patch("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
@inject
async def refresh(
    response: Response,
    refresh_token_usecase: FromDishka[RefreshTokenUseCase],
    settings: FromDishka[Settings],
) -> TokenResponse:
    """Эндпоинт для обновления refresh token."""
    log_info("Получен запрос на обновление токена")

    try:
        tokens = await refresh_token_usecase.execute()

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
            value=str(tokens.refresh_token),
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            httponly=True,
            secure=settings.ENVIRONMENT == "production",
            samesite="lax",
        )

        log_info("Токены успешно обновлены")
        return TokenResponse(**asdict(tokens))
    except Exception as e:
        log_error("Ошибка при обновлении токенов", error=e)
        raise AuthenticationException(message=str(e)) from e
