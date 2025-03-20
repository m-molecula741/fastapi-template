"""Тесты для use case выхода из системы."""

from datetime import UTC, datetime
from uuid import UUID

import pytest

from app.application.use_cases.auth.logout import LogoutUseCase
from app.domain.entities.auth import AuthSession
from app.domain.exceptions import RefreshTokenException


@pytest.mark.asyncio
async def test_logout_success(mock_uow):
    """Тест успешного выхода из системы."""
    # Arrange
    refresh_token = UUID("11111111-1111-1111-1111-111111111111")
    user_email = "test@example.com"

    # Создаем мок сессии
    session = AuthSession(
        uuid=UUID("00000000-0000-0000-0000-000000000000"),
        refresh_token=refresh_token,
        user_email=user_email,
        expires_at=datetime.now(UTC),
        created_at=datetime.now(UTC),
    )

    mock_uow.auth_sessions.find_by_refresh_token.return_value = session

    usecase = LogoutUseCase(mock_uow, refresh_token)

    # Act
    await usecase.execute()

    # Assert
    mock_uow.auth_sessions.find_by_refresh_token.assert_called_once_with(refresh_token)
    mock_uow.auth_sessions.delete_by_refresh_token.assert_called_once_with(
        refresh_token
    )
    assert mock_uow.commit.call_count == 1


@pytest.mark.asyncio
async def test_logout_token_not_found(mock_uow):
    """Тест выхода с несуществующим токеном."""
    # Arrange
    refresh_token = UUID("22222222-2222-2222-2222-222222222222")

    mock_uow.auth_sessions.find_by_refresh_token.return_value = None

    usecase = LogoutUseCase(mock_uow, refresh_token)

    # Act & Assert
    with pytest.raises(RefreshTokenException) as exc_info:
        await usecase.execute()

    assert "Сессия не найдена" in str(exc_info.value)
    mock_uow.auth_sessions.find_by_refresh_token.assert_called_once_with(refresh_token)
    mock_uow.auth_sessions.delete_by_refresh_token.assert_not_called()
