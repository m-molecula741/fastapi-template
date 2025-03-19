"""Тесты для use case логина пользователя."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone

from app.application.use_cases.auth.login import LoginUseCase
from app.domain.dto.auth import LoginDTO, TokenDTO
from app.domain.dto.user import UserDTO
from app.domain.entities.user import User
from app.domain.exceptions import AuthenticationException


@pytest.mark.asyncio(loop_scope="function")
async def test_login_success(mock_uow, mock_token_service, mock_user_entity):
    """Тест успешного логина пользователя."""
    # Arrange
    login_dto = LoginDTO(email="test@example.com", password="password123")
    
    mock_uow.users.find_by_email.return_value = mock_user_entity
    mock_token_service.generate_access_token.return_value = "access_token"
    mock_token_service.generate_refresh_token.return_value = "refresh_token"
    expires_at = datetime.now(timezone.utc)
    mock_token_service.get_refresh_token_expires_at.return_value = expires_at
    
    usecase = LoginUseCase(mock_uow, mock_token_service)
    
    # Act
    result = await usecase.execute(login_dto)
    
    # Assert
    assert isinstance(result, TokenDTO)
    assert result.access_token == "access_token"
    assert result.refresh_token == "refresh_token"
    assert result.expires_at == expires_at
    
    mock_uow.users.find_by_email.assert_called_once_with(login_dto.email)
    mock_token_service.generate_access_token.assert_called_once_with(login_dto.email)
    mock_token_service.generate_refresh_token.assert_called_once()
    mock_uow.auth_sessions.add.assert_called_once()


@pytest.mark.asyncio(loop_scope="function")
async def test_login_user_not_found(mock_uow, mock_token_service):
    """Тест логина с несуществующим пользователем."""
    # Arrange
    login_dto = LoginDTO(email="nonexistent@example.com", password="password123")
    
    mock_uow.users.find_by_email.return_value = None
    
    usecase = LoginUseCase(mock_uow, mock_token_service)
    
    # Act & Assert
    with pytest.raises(AuthenticationException) as exc_info:
        await usecase.execute(login_dto)
    
    assert "Неверный email или пароль" in str(exc_info.value)
    mock_uow.users.find_by_email.assert_called_once_with(login_dto.email)


@pytest.mark.asyncio(loop_scope="function")
async def test_login_wrong_password(mock_uow, mock_token_service, mock_user_entity):
    """Тест логина с неверным паролем."""
    # Arrange
    login_dto = LoginDTO(email="test@example.com", password="wrong_password")
    
    mock_user_entity.verify_password = MagicMock(return_value=False)
    mock_uow.users.find_by_email.return_value = mock_user_entity
    
    usecase = LoginUseCase(mock_uow, mock_token_service)
    
    # Act & Assert
    with pytest.raises(AuthenticationException) as exc_info:
        await usecase.execute(login_dto)
    
    assert "Неверный email или пароль" in str(exc_info.value)
    mock_user_entity.verify_password.assert_called_once_with(login_dto.password) 