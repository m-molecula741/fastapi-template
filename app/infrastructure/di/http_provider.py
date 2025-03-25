from dishka import FromDishka, Provider, Scope, provide

from app.application.use_cases.users.get_current_user import GetCurrentUserUseCase
from app.domain.entities.user import User


class HTTPProvider(Provider):
    """Провайдер HTTP-зависимостей."""

    def __init__(self) -> None:
        """Инициализирует провайдер."""
        super().__init__(scope=Scope.REQUEST)

    @provide
    async def current_user(
        self,
        get_current_user_usecase: FromDishka[GetCurrentUserUseCase],
    ) -> User:
        """Получает текущего пользователя."""
        user = await get_current_user_usecase.execute()
        return user
