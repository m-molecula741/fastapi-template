"""Роутеры для управления пользователями."""

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from app.application.use_cases.users.register import RegisterUserUseCase
from app.infrastructure.logging.logger import logger
from app.presentation.schemas.user import UserCreate, UserCreateResp

router = APIRouter()


@router.post(
    "/register", response_model=UserCreateResp, status_code=status.HTTP_201_CREATED
)
@inject
async def create_user(
    user_data: UserCreate,
    register_usecase: FromDishka[RegisterUserUseCase],
) -> UserCreateResp:
    """Создает нового пользователя."""
    try:
        user_email = await register_usecase.execute(user_data.to_domain())
        return UserCreateResp(email=user_email)
    except ValueError as e:
        logger.error(f"Ошибка при создании пользователя: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
