"""Use case для создания нового пользователя."""

from app.application.use_cases.base import UseCase
from app.domain.entities.user import User
from app.domain.exceptions import ValidationException
from app.domain.interfaces.uow import IUOW
from app.infrastructure.logging.logger import log_info, log_warning


class RegisterUserUseCase(UseCase[User]):
    """Use case для создания нового пользователя."""

    def __init__(self, uow: IUOW):
        """Инициализирует use case для создания пользователя."""
        self.uow = uow

    async def execute(self, user: User) -> str:
        """Создает нового пользователя."""
        log_info(f"Регистрация нового пользователя с email: {user.email}")

        async with self.uow:
            existing_user = await self.uow.users.find_by_email(user.email)
            if existing_user:
                log_warning(f"Пользователь с email {user.email} уже существует")
                raise ValidationException(
                    message=f"Пользователь с email {user.email} уже существует"
                )

            user_email = await self.uow.users.create_user(user=user)
            log_info(f"Пользователь с email {user_email} успешно зарегистрирован")

            return user_email
