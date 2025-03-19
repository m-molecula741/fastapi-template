"""Use case для создания нового пользователя."""
from app.domain.dto.user import UserCreateDTO, UserDTO
from app.domain.interfaces.uow import IUOW
from app.application.use_cases.base import UseCase
from app.infrastructure.logging.logger import logger


class RegisterUserUseCase(UseCase[UserDTO]):
    """Use case для создания нового пользователя."""
    
    def __init__(self, uow: IUOW):
        """Инициализирует use case для создания пользователя."""
        self.uow = uow
    
    async def execute(self, user_data: UserCreateDTO) -> str:
        """Создает нового пользователя."""

        async with self.uow:
            existing_user = await self.uow.users.find_by_email(user_data.email)
            if existing_user:
                logger.warning(f"Пользователь с email {user_data.email} уже существует")
                raise ValueError(f"Пользователь с email {user_data.email} уже существует")

            email = await self.uow.users.create_user(user=user_data.to_domain())
            
        return email
