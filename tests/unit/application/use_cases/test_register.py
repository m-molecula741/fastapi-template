"""Тесты для use case регистрации пользователя."""

import pytest

from app.application.use_cases.users.register import RegisterUserUseCase
from app.domain.entities.user import User
from app.domain.exceptions import ValidationException


@pytest.mark.asyncio(loop_scope="function")
async def test_register_success(mock_uow, mock_user):
    """Тест успешной регистрации пользователя."""
    # Arrange
    user_data = User(
        email="new@example.com",
        hashed_password="StrongPassword123!",
        is_active=True,
        is_verified=False,
    )

    # Пользователь не существует
    mock_uow.users.find_by_email.return_value = None

    # Успешное создание пользователя
    mock_uow.users.create_user.return_value = mock_user

    usecase = RegisterUserUseCase(mock_uow)

    # Act
    result = await usecase.execute(user_data)

    # Assert
    assert isinstance(result, User)
    assert result.email == mock_user.email

    mock_uow.users.find_by_email.assert_called_once_with(user_data.email)
    mock_uow.users.create_user.assert_called_once()


@pytest.mark.asyncio(loop_scope="function")
async def test_register_existing_email(mock_uow, mock_user_entity):
    """Тест регистрации с уже существующим email."""
    # Arrange
    existing_email = "existing@example.com"
    user_data = User(
        email=existing_email,
        hashed_password="StrongPassword123!",
        is_active=True,
        is_verified=False,
    )

    # Пользователь уже существует
    mock_uow.users.find_by_email.return_value = mock_user_entity

    usecase = RegisterUserUseCase(mock_uow)

    # Act & Assert
    with pytest.raises(ValidationException) as exc_info:
        await usecase.execute(user_data)

    assert f"Пользователь с email {existing_email} уже существует" in str(
        exc_info.value
    )
    mock_uow.users.find_by_email.assert_called_once_with(existing_email)
    mock_uow.users.create_user.assert_not_called()
