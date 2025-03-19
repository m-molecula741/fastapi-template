"""Схемы для авторизации."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr

from app.domain.dto.auth import LoginDTO, TokenDTO


class LoginRequest(BaseModel):
    """Схема запроса на авторизацию."""
    email: EmailStr
    password: str

    def to_dto(self) -> LoginDTO:
        """Преобразует Pydantic схему в DTO."""
        return LoginDTO(
            email=self.email,
            password=self.password
        )

class TokenResponse(BaseModel):
    """Схема ответа на авторизацию."""
    access_token: str
    refresh_token: str

    @staticmethod
    def from_dto(dto: TokenDTO) -> TokenResponse:
        """Преобразует DTO в Pydantic схему."""
        return TokenResponse(
            access_token=dto.access_token,
            refresh_token=dto.refresh_token
        )
