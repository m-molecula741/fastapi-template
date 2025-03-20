"""API для работы с пользователями (требует авторизации)."""

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from app.domain.dto.user import UserDTO
from app.infrastructure.logging.logger import log_info
from app.presentation.schemas.user import UserResponse

router = APIRouter()


@router.get("/me", response_model=None, status_code=status.HTTP_200_OK)
@inject
async def get_current_user_endpoint(
    current_user: FromDishka[UserDTO],
):
    """Получает информацию о текущем авторизованном пользователе."""
    log_info(
        "Получен запрос на получение текущего пользователя", email=current_user.email
    )
    return UserResponse(
        email=current_user.email,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )
