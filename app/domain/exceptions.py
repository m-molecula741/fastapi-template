"""Домен-специфичные исключения для чистой архитектуры."""

from typing import Any


class DomainException(Exception):
    """Базовое исключение для всех доменных ошибок."""

    def __init__(
        self,
        message: str = "Произошла ошибка в домене",
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationException(DomainException):
    """Исключение для ошибок аутентификации."""

    def __init__(
        self,
        message: str = "Ошибка аутентификации",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, details)


class NotFoundException(DomainException):
    """Исключение для случаев, когда объект не найден."""

    def __init__(
        self,
        entity_type: str,
        entity_id: Any,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        message = message or f"{entity_type} с идентификатором {entity_id} не найден"
        super().__init__(message, details)


class ValidationException(DomainException):
    """Исключение для ошибок валидации."""

    def __init__(
        self, message: str = "Ошибка валидации", details: dict[str, Any] | None = None
    ):
        super().__init__(message, details)


class AuthorizationException(DomainException):
    """Исключение для ошибок авторизации (прав доступа)."""

    def __init__(
        self,
        message: str = "Недостаточно прав для выполнения операции",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, details)


class BusinessRuleException(DomainException):
    """Исключение для нарушения бизнес-правил."""

    def __init__(
        self,
        message: str = "Нарушение бизнес-правила",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, details)


class TokenException(AuthenticationException):
    """Исключение для ошибок, связанных с JWT токенами."""

    def __init__(
        self, message: str = "Ошибка в токене", details: dict[str, Any] | None = None
    ):
        super().__init__(message, details)


class RefreshTokenException(TokenException):
    """Исключение для ошибок, связанных с refresh-токенами."""

    def __init__(
        self,
        message: str = "Ошибка в refresh-токене",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, details)
