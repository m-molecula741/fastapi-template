"""API для работы с авторизацией."""

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Response, status

from app.application.use_cases.auth.logout import LogoutUseCase
from app.domain.dto.user import UserDTO
from app.domain.exceptions import AuthenticationException
from app.infrastructure.logging.logger import log_error, log_info

router = APIRouter()


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def logout(
    response: Response,
    logout_usecase: FromDishka[LogoutUseCase],
    current_user: FromDishka[UserDTO]
) -> None:
    """Выполняет выход пользователя из системы."""
    log_info("Получен запрос на выход из системы", email=current_user.email)

    try:
        await logout_usecase.execute()
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")

        log_info("Пользователь успешно вышел из системы", email=current_user.email)
    except Exception as e:
        log_error("Ошибка при выходе из системы", error=e, email=current_user.email)
        raise AuthenticationException(message=str(e)) from e
