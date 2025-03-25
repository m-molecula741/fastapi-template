from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from uuid_extensions import uuid7

from app.infrastructure.consts import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


class TokenService:
    """Сервис для работы с токенами."""

    def __init__(self, secret_key: str, algorithm: str = JWT_ALGORITHM):
        """Инициализирует сервис для работы с токенами."""
        self.secret_key = secret_key
        self.algorithm = algorithm

    def generate_access_token(self, email: str) -> str:
        """Генерирует access token."""
        payload = {
            "sub": email,
            "exp": datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        encoded_jwt = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return f"{encoded_jwt}"

    def decode_access_token(self, token: str) -> dict:
        """Декодирует access token."""
        if token.startswith("Bearer "):
            token = token[7:]
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

    def generate_refresh_token(self) -> UUID:
        """Генерирует refresh token."""
        return uuid7()

    def get_refresh_token_expires_at(self) -> datetime:
        """Возвращает срок действия refresh token."""
        return datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
