"""API для работы с пользователями (требует авторизации)."""

from dataclasses import asdict

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from app.domain.entities.user import User
from app.infrastructure.logging.logger import log_info
from app.presentation.schemas.user import UserResponse

router = APIRouter()


@router.get("/me", response_model=None, status_code=status.HTTP_200_OK)
@inject
async def get_current_user_endpoint(
    current_user: FromDishka[User],
):
    """Получает информацию о текущем авторизованном пользователе."""
    log_info(
        "Получен запрос на получение текущего пользователя", email=current_user.email
    )
    return UserResponse(**asdict(current_user), exclude={"hashed_password"})
