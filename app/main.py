"""Главный файл приложения."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.infrastructure.logging.logger import logger, log_info
from app.infrastructure.database.session import create_tables
from app.presentation.api.router import api_public_router, api_private_router
from app.presentation.exception_handlers import register_exception_handlers
from app.infrastructure.config.settings import get_settings

settings = get_settings()

# Создаем приложение FastAPI
app = FastAPI(
    title="User Management API",
    description="API для управления пользователями",
    version="1.0.0",
)

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Регистрируем обработчики исключений
register_exception_handlers(app)

# Регистрируем API роутеры
app.include_router(api_public_router)
app.include_router(api_private_router)


# Переопределяем схему OpenAPI для добавления security к приватным эндпоинтам
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Добавляем компонент безопасности
    openapi_schema["components"] = openapi_schema.get("components", {})
    openapi_schema["components"]["securitySchemes"] = {
        "cookieAuth": {
            "type": "apiKey",
            "in": "cookie",
            "name": "access_token"
        }
    }
    
    # Добавляем требование безопасности для всех приватных путей
    for path, path_item in openapi_schema["paths"].items():
        if path.startswith("/api/private"):
            for method in path_item:
                path_item[method]["security"] = [{"cookieAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Переопределяем схему OpenAPI
app.openapi = custom_openapi


@app.get("/")
async def health_check():
    """Проверка работоспособности API."""
    log_info("Запрос проверки работоспособности API")
    return {"status": "ok", "message": "API работает"}


@app.on_event("startup")
async def startup():
    """Действия при запуске приложения."""
    log_info("Приложение запущено", environment=settings.ENVIRONMENT)
    # Создаем таблицы в базе данных
    await create_tables()


@app.on_event("shutdown")
async def shutdown():
    """Действия при остановке приложения."""
    log_info("Приложение остановлено")
