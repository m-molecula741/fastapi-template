"""SQL реализация репозитория пользователей."""
from typing import Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.interfaces.user_repo import IUserRepository
from app.infrastructure.database.models.user import UserModel as UserModel


class UserRepository(IUserRepository):
    """SQLAlchemy реализация репозитория пользователей."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """Находит пользователля по email."""
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()
        
        if user_model:
            return User(
                email=user_model.email,
                hashed_password=user_model.hashed_password,
                is_active=user_model.is_active,
                is_verified=user_model.is_verified,
                created_at=user_model.created_at,
                updated_at=user_model.updated_at,
            )
        return None
    
    async def create_user(self, user: User) -> str:
        """Создает пользователя в базе данных и возвращает первичный ключ (email)."""
        result = await self.session.execute(
            insert(UserModel).values(**user.to_dict()).returning(UserModel.email)
        )
        email = result.scalar_one()

        return email
