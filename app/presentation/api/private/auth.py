"""API для работы с авторизацией."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.application.use_cases.auth.logout import LogoutUseCase
from app.domain.dto.user import UserDTO
from app.domain.exceptions import AuthenticationException
from app.infrastructure.logging.logger import log_error, log_info
from app.presentation.api.dependencies import (
    get_current_user,
    get_logout_usecase,
    get_refresh_token_from_cookie,
)

router = APIRouter()


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    usecase: Annotated[LogoutUseCase, Depends(get_logout_usecase)],
    response: Response,
    current_user: Annotated[UserDTO, Depends(get_current_user)],
    refresh_token: str = Depends(get_refresh_token_from_cookie),
) -> None:
    """Выполняет выход пользователя из системы."""
    log_info("Получен запрос на выход из системы", email=current_user.email)

    try:
        await usecase.execute(refresh_token)
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")

        log_info("Пользователь успешно вышел из системы", email=current_user.email)
    except Exception as e:
        log_error("Ошибка при выходе из системы", error=e, email=current_user.email)
        raise AuthenticationException(message=str(e)) from e
