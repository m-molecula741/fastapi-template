"""Получение текущего пользователя."""

from app.domain.dto.user import UserDTO
from app.domain.interfaces.token_service import ITokenService
from app.domain.interfaces.uow import IUOW


class GetCurrentUserUseCase:
    """Получение текущего пользователя."""

    def __init__(self, uow: IUOW, token_service: ITokenService):
        self.uow = uow
        self.token_service = token_service

    async def execute(self, token: str) -> UserDTO:
        """Возвращает текущего пользователя."""
        try:
            payload = self.token_service.decode_access_token(token)
            email = payload.get("sub")
            if not email:
                raise ValueError("Не удалось извлечь email из токена")
        except Exception as e:
            raise ValueError(f"Ошибка при декодировании токена: {str(e)}") from e

        current_user = await self.uow.users.find_by_email(email=email)
        if not current_user:
            raise ValueError("Пользователь не найден")

        return UserDTO.from_domain(current_user)
