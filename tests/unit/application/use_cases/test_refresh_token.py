"""Тесты для use case обновления refresh токена."""

from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest

from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.domain.entities.auth import AuthSession, Token
from app.domain.exceptions import RefreshTokenException


@pytest.mark.asyncio(loop_scope="function")
async def test_refresh_token_success(mock_uow, mock_token_service, mock_user_entity):
    """Тест успешного обновления токена."""
    # Arrange
    refresh_token = UUID("11111111-1111-1111-1111-111111111111")
    user_email = "test@example.com"

    # Создаем мок сессии
    expires_at = datetime.now(UTC) + timedelta(days=7)
    session = AuthSession(
        uuid=UUID("00000000-0000-0000-0000-000000000000"),
        refresh_token=refresh_token,
        user_email=user_email,
        expires_at=expires_at,
        created_at=datetime.now(UTC),
    )

    mock_uow.auth_sessions.find_by_refresh_token.return_value = session
    mock_uow.users.find_by_email.return_value = mock_user_entity

    # Настраиваем моки для новых токенов
    new_access_token = "new_access_token"
    new_refresh_token = UUID("44444444-4444-4444-4444-444444444444")
    new_expires_at = datetime.now(UTC) + timedelta(days=14)

    mock_token_service.generate_access_token.return_value = new_access_token
    mock_token_service.generate_refresh_token.return_value = new_refresh_token
    mock_token_service.get_refresh_token_expires_at.return_value = new_expires_at

    usecase = RefreshTokenUseCase(mock_uow, mock_token_service, refresh_token)

    # Act
    result = await usecase.execute()

    # Assert
    assert isinstance(result, Token)
    assert result.access_token == new_access_token
    assert result.refresh_token == new_refresh_token

    mock_uow.auth_sessions.find_by_refresh_token.assert_called_once_with(refresh_token)
    mock_uow.users.find_by_email.assert_called_once_with(user_email)
    mock_token_service.generate_access_token.assert_called_once_with(user_email)
    mock_token_service.generate_refresh_token.assert_called_once()
    mock_uow.auth_sessions.update_refresh_token.assert_called_once_with(
        session.uuid, new_refresh_token, new_expires_at
    )
    # Коммит теперь происходит автоматически при выходе из контекстного менеджера
    # mock_uow.commit.assert_called_once()


@pytest.mark.asyncio(loop_scope="function")
async def test_refresh_token_not_found(mock_uow, mock_token_service):
    """Тест обновления с несуществующим токеном."""
    # Arrange
    refresh_token = UUID("22222222-2222-2222-2222-222222222222")

    mock_uow.auth_sessions.find_by_refresh_token.return_value = None

    usecase = RefreshTokenUseCase(mock_uow, mock_token_service, refresh_token)

    # Act & Assert
    with pytest.raises(RefreshTokenException) as exc_info:
        await usecase.execute()

    assert "Недействительный refresh token" in str(exc_info.value)
    mock_uow.auth_sessions.find_by_refresh_token.assert_called_once_with(refresh_token)
    # Коммит не должен вызываться при ошибке


@pytest.mark.asyncio(loop_scope="function")
async def test_refresh_token_expired(mock_uow, mock_token_service):
    """Тест обновления с истекшим токеном."""
    # Arrange
    refresh_token = UUID("33333333-3333-3333-3333-333333333333")
    user_email = "test@example.com"

    # Создаем мок сессии с истекшим сроком действия
    expired_time = datetime.now(UTC) - timedelta(days=1)
    session = AuthSession(
        uuid=UUID("00000000-0000-0000-0000-000000000000"),
        refresh_token=refresh_token,
        user_email=user_email,
        expires_at=expired_time,
        created_at=datetime.now(UTC) - timedelta(days=14),
    )

    mock_uow.auth_sessions.find_by_refresh_token.return_value = session

    usecase = RefreshTokenUseCase(mock_uow, mock_token_service, refresh_token)

    # Act & Assert
    with pytest.raises(RefreshTokenException) as exc_info:
        await usecase.execute()

    assert "Срок действия refresh token истек" in str(exc_info.value)
    mock_uow.auth_sessions.find_by_refresh_token.assert_called_once_with(refresh_token)
    # Должен удалить истекшую сессию
    mock_uow.auth_sessions.remove.assert_called_once_with(session.uuid)
    # Коммит теперь происходит автоматически при выходе из контекстного менеджера
