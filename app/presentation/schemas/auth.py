"""Схемы для авторизации."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Схема запроса на авторизацию."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Схема ответа на авторизацию."""

    access_token: str
    refresh_token: UUID
