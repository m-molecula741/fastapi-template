"""API для работы с авторизацией."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.application.use_cases.auth.logout import LogoutUseCase
from app.domain.dto.user import UserDTO
from app.presentation.api.dependencies import get_current_user, get_logout_usecase, get_refresh_token_from_cookie

router = APIRouter()

@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    usecase: Annotated[LogoutUseCase, Depends(get_logout_usecase)],
    response: Response,
    current_user: Annotated[UserDTO, Depends(get_current_user)],
    refresh_token: str = Depends(get_refresh_token_from_cookie),
) -> None:
    """Выполняет выход пользователя из системы."""
    try:
        await usecase.execute(refresh_token)
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
