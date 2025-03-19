"""Роутеры для управления пользователями."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.use_cases.users.register import RegisterUserUseCase
from app.presentation.api.dependencies import get_register_usecase
from app.infrastructure.logging.logger import logger
from app.presentation.schemas.user import UserCreate, UserCreateResp

router = APIRouter()


@router.post("/register", response_model=UserCreateResp, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    create_user_usecase: Annotated[RegisterUserUseCase, Depends(get_register_usecase)],
):
    """Создает нового пользователя."""  
    try:
        email = await create_user_usecase.execute(user_data.to_dto())
        return UserCreateResp(email=email)
    except ValueError as e:
        logger.error(f"Ошибка при создании пользователя: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
