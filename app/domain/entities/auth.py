from datetime import datetime
from typing import Optional
from uuid import UUID

class AuthSession:
    """Доменная модель авторизационной сессии."""

    def __init__(
        self,
        uuid: UUID,
        refresh_token: UUID,
        expires_at: datetime,
        user_email: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """Инициализирует авторизационную сессию."""
        self.uuid = uuid
        self.refresh_token = refresh_token
        self.expires_at = expires_at
        self.user_email = user_email
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        """Преобразует авторизационную сессию в словарь."""
        return {
            "uuid": self.uuid,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at,
            "user_email": self.user_email,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
