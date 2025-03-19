"""Обработчики исключений для FastAPI."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.domain.exceptions import (
    AuthenticationException,
    AuthorizationException,
    BusinessRuleException,
    DomainException,
    NotFoundException,
    RefreshTokenException,
    TokenException,
    ValidationException,
)
from app.infrastructure.logging.logger import log_error


def register_exception_handlers(app: FastAPI) -> None:
    """Регистрирует обработчики исключений для приложения FastAPI."""

    @app.exception_handler(ValidationException)
    async def validation_exception_handler(request: Request, exc: ValidationException):
        log_error("Ошибка валидации", error=exc, path=request.url.path)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message, "errors": exc.details},
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(
        request: Request, exc: ValidationError
    ):
        log_error("Ошибка валидации Pydantic", error=exc, path=request.url.path)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Ошибка валидации данных", "errors": exc.errors()},
        )

    @app.exception_handler(AuthenticationException)
    async def authentication_exception_handler(
        request: Request, exc: AuthenticationException
    ):
        log_error("Ошибка аутентификации", error=exc, path=request.url.path)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": exc.message}
        )

    @app.exception_handler(TokenException)
    async def token_exception_handler(request: Request, exc: TokenException):
        log_error("Ошибка в токене", error=exc, path=request.url.path)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": exc.message}
        )

    @app.exception_handler(RefreshTokenException)
    async def refresh_token_exception_handler(
        request: Request, exc: RefreshTokenException
    ):
        log_error("Ошибка в refresh-токене", error=exc, path=request.url.path)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": exc.message}
        )

    @app.exception_handler(AuthorizationException)
    async def authorization_exception_handler(
        request: Request, exc: AuthorizationException
    ):
        log_error("Ошибка авторизации", error=exc, path=request.url.path)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN, content={"detail": exc.message}
        )

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        log_error("Объект не найден", error=exc, path=request.url.path)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": exc.message}
        )

    @app.exception_handler(BusinessRuleException)
    async def business_rule_exception_handler(
        request: Request, exc: BusinessRuleException
    ):
        log_error("Нарушение бизнес-правила", error=exc, path=request.url.path)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.message, "errors": exc.details},
        )

    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        log_error("Доменная ошибка", error=exc, path=request.url.path)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message, "errors": exc.details},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        log_error("Необработанная ошибка", error=exc, path=request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Внутренняя ошибка сервера"},
        )
