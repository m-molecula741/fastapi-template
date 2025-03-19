"""Тесты для use case выхода из системы."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone
from uuid import UUID

from app.application.use_cases.auth.logout import LogoutUseCase
from app.domain.entities.auth import AuthSession
from app.domain.exceptions import RefreshTokenException


@pytest.mark.asyncio(loop_scope="function")
async def test_logout_success(mock_uow):
    """Тест успешного выхода из системы."""
    # Arrange
    refresh_token = "valid_refresh_token"
    user_email = "test@example.com"
    
    # Создаем мок сессии
    session = AuthSession(
        uuid=UUID('00000000-0000-0000-0000-000000000000'),
        refresh_token=refresh_token,
        user_email=user_email,
        expires_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc)
    )
    
    mock_uow.auth_sessions.find_by_refresh_token.return_value = session
    
    usecase = LogoutUseCase(mock_uow)
    
    # Act
    await usecase.execute(refresh_token)
    
    # Assert
    mock_uow.auth_sessions.find_by_refresh_token.assert_called_once_with(refresh_token)
    mock_uow.auth_sessions.delete_by_refresh_token.assert_called_once_with(refresh_token)


@pytest.mark.asyncio(loop_scope="function")
async def test_logout_token_not_found(mock_uow):
    """Тест выхода с несуществующим токеном."""
    # Arrange
    refresh_token = "nonexistent_refresh_token"
    
    mock_uow.auth_sessions.find_by_refresh_token.return_value = None
    
    usecase = LogoutUseCase(mock_uow)
    
    # Act & Assert
    with pytest.raises(RefreshTokenException) as exc_info:
        await usecase.execute(refresh_token)
    
    assert "Сессия не найдена" in str(exc_info.value)
    mock_uow.auth_sessions.find_by_refresh_token.assert_called_once_with(refresh_token)
    mock_uow.auth_sessions.delete_by_refresh_token.assert_not_called() 