"""Схемы данных для пользователей."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.domain.entities.user import User, pwd_context


class UserCreate(BaseModel):
    """Схема для создания пользователя."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)

    def to_domain(self) -> User:
        """Конвертирует схему в доменную модель."""
        return User(
            email=self.email,
            hashed_password=pwd_context.hash(self.password),
        )


class UserCreateResp(BaseModel):
    """Схема ответа на создание пользователя."""

    email: str


class UserBase(BaseModel):
    """Базовая схема пользователя."""

    email: str


class UserUpdate(UserBase):
    """Схема для обновления пользователя."""

    password: str = Field(None, min_length=8, max_length=100)
    is_active: bool = None
    is_verified: bool = None


class UserResponse(UserBase):
    """Схема ответа для пользователя."""

    is_active: bool
    is_verified: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
