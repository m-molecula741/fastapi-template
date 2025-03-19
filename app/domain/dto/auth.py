from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class LoginDTO:
    """DTO для авторизации."""

    email: str
    password: str


@dataclass
class TokenDTO:
    """DTO для ответа авторизации."""

    access_token: str
    refresh_token: UUID
    expires_at: datetime
