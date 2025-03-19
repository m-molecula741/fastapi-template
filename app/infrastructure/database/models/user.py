"""Модель пользователя для SQL."""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.models.base import Base, TimestampMixin


class UserModel(Base, TimestampMixin):
    """Модель пользователя для SQL."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(100), primary_key=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        """Возвращает строковое представление модели."""
        return f"User(email={self.email})"
