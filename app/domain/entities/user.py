"""Доменная модель пользователя."""

from dataclasses import dataclass
from datetime import UTC, datetime

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class User:
    """Доменная модель пользователя."""

    email: str
    hashed_password: str
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime | None = datetime.now(UTC)
    updated_at: datetime | None = None

    def verify_password(self, plain_password: str) -> bool:
        """Проверяет, совпадает ли переданный пароль с хэшированным паролем."""
        return pwd_context.verify(plain_password, self.hashed_password)
