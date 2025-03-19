"""Data Transfer Objects для пользователей."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from app.domain.entities.user import User, pwd_context


@dataclass
class UserCreateDTO:
    """DTO для создания пользователя."""
    email: str
    password: str
    is_active: bool = True
    is_verified: bool = False

    def to_domain(self,) -> User:
        """Преобразует DTO в доменную сущность."""
        return User(
            email=self.email,
            hashed_password=pwd_context.hash(self.password),
            is_active=self.is_active,
            is_verified=self.is_verified,
            created_at=datetime.now(timezone.utc)
        )


@dataclass
class UserDTO:
    """DTO для передачи данных пользователя."""
    email: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    @staticmethod
    def from_domain(user: User) -> UserDTO:
        """Преобразует доменную сущность в DTO."""
        return UserDTO(
            email=user.email,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
