"""Use case для создания нового пользователя."""

from app.application.use_cases.base import UseCase
from app.domain.dto.user import UserCreateDTO, UserDTO
from app.domain.exceptions import ValidationException
from app.domain.interfaces.uow import IUOW
from app.infrastructure.logging.logger import log_info, log_warning


class RegisterUserUseCase(UseCase[UserDTO]):
    """Use case для создания нового пользователя."""

    def __init__(self, uow: IUOW):
        """Инициализирует use case для создания пользователя."""
        self.uow = uow

    async def execute(self, user_data: UserCreateDTO) -> UserDTO:
        """Создает нового пользователя."""
        log_info(f"Регистрация нового пользователя с email: {user_data.email}")

        async with self.uow:
            existing_user = await self.uow.users.find_by_email(user_data.email)
            if existing_user:
                log_warning(f"Пользователь с email {user_data.email} уже существует")
                raise ValidationException(
                    message=f"Пользователь с email {user_data.email} уже существует"
                )

            # Создаем доменную модель пользователя
            user_domain = user_data.to_domain()

            # Создаем пользователя в БД
            new_user = await self.uow.users.create_user(user=user_domain)

            log_info(f"Пользователь с email {user_data.email} успешно зарегистрирован")

            return new_user
