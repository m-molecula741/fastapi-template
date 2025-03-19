from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import UUID as SQLAlchemyUUID
from sqlalchemy.types import DateTime

from app.infrastructure.database.models.base import Base, TimestampMixin


class AuthSessionModel(Base, TimestampMixin):
    """ORM-модель авторизационной сессии пользователя."""

    __tablename__ = "auth_sessions"

    uuid: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True)
    refresh_token: Mapped[UUID] = mapped_column(SQLAlchemyUUID, index=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    user_email: Mapped[str] = mapped_column(
        String(320), ForeignKey("users.email", ondelete="CASCADE")
    )
