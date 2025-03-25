from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class AuthSession:
    """Доменная модель авторизационной сессии."""

    uuid: UUID
    refresh_token: UUID
    expires_at: datetime
    user_email: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class Token:
    """Доменная модель токена."""

    access_token: str
    refresh_token: UUID
