"""Конфигурация для pytest."""

import logging
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest

from app.domain.dto.auth import TokenDTO
from app.domain.dto.user import UserDTO
from app.domain.entities.user import User
from app.domain.interfaces.token_service import ITokenService
from app.domain.interfaces.uow import IUOW


@pytest.fixture(autouse=True)
def disable_logging():
    """Отключает логирование во время тестов."""
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


@pytest.fixture
def mock_uow() -> MagicMock:
    """Создает мок для Unit of Work."""
    uow = MagicMock(spec=IUOW)

    async def async_exit(exc_type=None, exc_val=None, exc_tb=None):
        if exc_type is None:
            await uow.commit()
        else:
            await uow.rollback()
        return False

    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(side_effect=async_exit)
    uow.commit = AsyncMock()
    uow.rollback = AsyncMock()

    # Моки для репозиториев
    uow.users = MagicMock()
    uow.users.find_by_email = AsyncMock()
    uow.users.create_user = AsyncMock()

    uow.auth_sessions = MagicMock()
    uow.auth_sessions.add = AsyncMock()
    uow.auth_sessions.find_by_refresh_token = AsyncMock()
    uow.auth_sessions.remove = AsyncMock()
    uow.auth_sessions.delete_by_refresh_token = AsyncMock()
    uow.auth_sessions.update_refresh_token = AsyncMock()

    return uow


@pytest.fixture
def mock_token_service() -> MagicMock:
    """Создает мок для сервиса токенов."""
    service = MagicMock(spec=ITokenService)
    service.generate_access_token = MagicMock(return_value="mock_access_token")
    mock_uuid = UUID("00000000-0000-0000-0000-000000000000")
    service.generate_refresh_token = MagicMock(return_value=mock_uuid)
    service.get_refresh_token_expires_at = MagicMock(
        return_value=datetime.now(UTC) + timedelta(days=7)
    )
    service.verify_access_token = MagicMock()
    service.get_user_email_from_token = MagicMock()
    service.decode_access_token = MagicMock(return_value={"sub": "test@example.com"})

    return service


@pytest.fixture
def mock_user() -> UserDTO:
    """Создает мок пользователя."""
    return UserDTO(
        email="test@example.com",
        is_active=True,
        is_verified=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )


@pytest.fixture
def mock_user_entity() -> User:
    """Создает мок сущности пользователя."""
    user = User(
        email="test@example.com",
        hashed_password="$2b$12$abc123hashvalue456",
        is_active=True,
        is_verified=True,
    )
    # Мокируем метод verify_password для тестов
    user.verify_password = MagicMock(return_value=True)
    return user


@pytest.fixture
def mock_tokens() -> TokenDTO:
    """Создает мок токенов."""
    return TokenDTO(
        access_token="mock_access_token",
        refresh_token=UUID("00000000-0000-0000-0000-000000000000"),
        expires_at=datetime.now(UTC) + timedelta(days=7),
    )
