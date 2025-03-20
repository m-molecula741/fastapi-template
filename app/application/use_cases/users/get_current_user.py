"""Получение текущего пользователя."""

from app.domain.dto.user import UserDTO
from app.domain.exceptions import AuthenticationException
from app.domain.interfaces.token_service import ITokenService
from app.domain.interfaces.uow import IUOW


class GetCurrentUserUseCase:
    """Получение текущего пользователя."""

    def __init__(self, uow: IUOW, token_service: ITokenService, token: str):
        self.uow = uow
        self.token_service = token_service
        self.token = token

    async def execute(self) -> UserDTO:
        """Возвращает текущего пользователя."""
        try:
            if not self.token or self.token == "":
                raise AuthenticationException("Access токен не найден")
            payload = self.token_service.decode_access_token(self.token)
            email = payload.get("sub")
            if not email:
                raise AuthenticationException("Не удалось извлечь email из токена")
        except Exception as e:
            error_msg = f"Ошибка при декодировании токена: {str(e)}"
            raise AuthenticationException(error_msg) from e

        current_user = await self.uow.users.find_by_email(email=email)
        if not current_user:
            raise AuthenticationException("Пользователь не найден")

        return UserDTO.from_domain(current_user)
