"""Тесты для use case логина пользователя."""

from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock

import pytest

from app.application.use_cases.auth.login import LoginUseCase
from app.domain.entities.auth import Token
from app.domain.entities.user import User, pwd_context
from app.domain.exceptions import AuthenticationException
from app.domain.interfaces.token_service import ITokenService
from app.domain.interfaces.uow import IUOW


@pytest.mark.asyncio
async def test_login_success(mock_uow: IUOW, mock_token_service: ITokenService):
    """Тест успешного логина пользователя."""
    # Arrange
    email = "test@example.com"
    password = "password123"
    hashed_password = pwd_context.hash("password123")

    user = User(
        email=email,
        hashed_password=hashed_password,
        is_active=True,
        is_verified=True,
    )

    mock_uow.users.find_by_email.return_value = user
    mock_token_service.generate_access_token.return_value = "access_token"
    mock_token_service.generate_refresh_token.return_value = "refresh_token"
    expires_at = datetime.now(UTC) + timedelta(days=7)
    mock_token_service.get_refresh_token_expires_at.return_value = expires_at

    usecase = LoginUseCase(mock_uow, mock_token_service)

    # Act
    result = await usecase.execute(email=email, password=password)

    # Assert
    assert isinstance(result, Token)
    assert result.access_token == "access_token"
    assert result.refresh_token == "refresh_token"

    mock_uow.users.find_by_email.assert_called_once_with(email)
    mock_token_service.generate_access_token.assert_called_once_with(email)
    mock_token_service.generate_refresh_token.assert_called_once()
    mock_uow.auth_sessions.add.assert_called_once()


@pytest.mark.asyncio
async def test_login_user_not_found(mock_uow: IUOW, mock_token_service: ITokenService):
    """Тест логина с несуществующим пользователем."""
    # Arrange
    email = "nonexistent@example.com"
    password = "password123"

    mock_uow.users.find_by_email.return_value = None

    usecase = LoginUseCase(mock_uow, mock_token_service)

    # Act & Assert
    with pytest.raises(AuthenticationException) as exc_info:
        await usecase.execute(email=email, password=password)

    assert "Неверный email или пароль" in str(exc_info.value)
    mock_uow.users.find_by_email.assert_called_once_with(email)


@pytest.mark.asyncio
async def test_login_wrong_password(
    mock_uow: IUOW, mock_token_service: ITokenService, mock_user_entity: User
):
    """Тест логина с неверным паролем."""
    # Arrange
    email = "test@example.com"
    password = "wrong_password"

    mock_user_entity.verify_password = MagicMock(return_value=False)
    mock_uow.users.find_by_email.return_value = mock_user_entity

    usecase = LoginUseCase(mock_uow, mock_token_service)

    # Act & Assert
    with pytest.raises(AuthenticationException) as exc_info:
        await usecase.execute(email=email, password=password)

    assert "Неверный email или пароль" in str(exc_info.value)
    mock_user_entity.verify_password.assert_called_once_with(password)
