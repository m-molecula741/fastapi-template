"""Схемы API для работы с пользователями."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.domain.dto.user import UserCreateDTO, UserDTO


class UserBase(BaseModel):
    """Базовая схема пользователя."""

    email: EmailStr
    is_active: bool | None = True
    is_verified: bool | None = False


class UserCreate(BaseModel):
    """Схема для создания пользователя."""

    email: EmailStr
    password: str = Field(..., min_length=8)

    def to_dto(self) -> UserCreateDTO:
        """Преобразует схему в DTO."""
        return UserCreateDTO(email=self.email, password=self.password)


class UserCreateResp(BaseModel):
    """Схема ответа при создании юзера."""

    email: EmailStr


class UserRead(UserBase):
    """Схема для чтения данных пользователя."""

    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_dto(dto: UserDTO) -> UserRead:
        """Преобразует DTO в схему."""
        return UserRead(
            email=dto.email,
            is_active=dto.is_active,
            is_verified=dto.is_verified,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

    class Config:
        """Конфигурация модели."""

        from_attributes = True
