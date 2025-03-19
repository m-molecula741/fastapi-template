"""Доменная модель пользователя."""
from datetime import datetime
from typing import Optional
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User:
    """Доменная модель пользователя."""
    
    def __init__(
        self,
        email: str,
        hashed_password: str,
        is_active: bool = True,
        is_verified: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """Инициализирует пользователя."""
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.is_verified = is_verified
        self.created_at = created_at
        self.updated_at = updated_at

    def verify_password(self, plain_password: str) -> bool:
        """Проверяет, совпадает ли переданный пароль с хэшированным паролем пользователя."""
        return pwd_context.verify(plain_password, self.hashed_password)
    
    def to_dict(self):
        """Преобразует пользователя в словарь."""
        return {
            "email": self.email,
            "hashed_password": self.hashed_password,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
