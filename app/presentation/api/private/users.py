"""Роутеры для управления пользователями."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.domain.dto.user import UserDTO
from app.presentation.api.dependencies import get_current_user
from app.presentation.schemas.user import UserRead

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def get_current_user(
    current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    """Получает текущего пользователя."""
    return UserRead.from_dto(current_user)
