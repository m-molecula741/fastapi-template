from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.presentation.api.dependencies import get_login_usecase, get_refresh_token_from_cookie, get_refresh_token_usecase
from app.presentation.schemas.auth import LoginRequest, TokenResponse
from app.infrastructure.config.settings import get_settings


router = APIRouter()


settings = get_settings()


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    login_usecase: Annotated[LoginUseCase, Depends(get_login_usecase)],
    response: Response
):
    """Эндпоинт для авторизации пользователя."""
    try:
        login_dto = login_data.to_dto()
        
        tokens = await login_usecase.execute(login_dto)
        
        response.set_cookie(
            key="access_token",
            value=tokens.access_token,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=False,
            samesite="lax"
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            httponly=True,
            secure=False,
            samesite="lax"
        )
        
        return TokenResponse.from_dto(tokens)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.patch("/refresh", response_model=TokenResponse)
async def refresh(
    refresh_token: Annotated[str, Depends(get_refresh_token_from_cookie)],
    refresh_token_usecase: Annotated[RefreshTokenUseCase, Depends(get_refresh_token_usecase)],
    response: Response
):
    """Эндпоинт для обновления refresh token."""
    try:
        tokens = await refresh_token_usecase.execute(refresh_token)

        response.set_cookie(
            key="access_token",
            value=tokens.access_token,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=False,
            samesite="lax"
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            httponly=True,
            secure=False,
            samesite="lax"
        )
        
        return TokenResponse.from_dto(tokens)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
