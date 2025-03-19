"""Главный файл приложения."""
from fastapi import FastAPI

from app.infrastructure.logging.logger import logger
from app.infrastructure.database.session import create_tables
from app.presentation.api.router import api_public_router, api_private_router

# Создаем приложение FastAPI
app = FastAPI(
    title="User Management API",
    description="API для управления пользователями",
    version="1.0.0",
)

# Регистрируем API роутеры
app.include_router(api_public_router)
app.include_router(api_private_router)


@app.get("/")
async def health_check():
    """Проверка работоспособности API."""
    logger.info("Запрос проверки работоспособности API")
    return {"status": "ok", "message": "API работает"}


@app.on_event("startup")
async def startup():
    """Действия при запуске приложения."""
    logger.info("Приложение запущено")
    # Создаем таблицы в базе данных
    await create_tables()


@app.on_event("shutdown")
async def shutdown():
    """Действия при остановке приложения."""
    logger.info("Приложение остановлено")
