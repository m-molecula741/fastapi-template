"""Главный файл приложения."""

from contextlib import asynccontextmanager
from pathlib import Path

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.infrastructure.config.settings import get_settings
from app.infrastructure.database.session import create_tables
from app.infrastructure.di.container import container
from app.infrastructure.logging.logger import log_info
from app.presentation.api.router import api_private_router, api_public_router
from app.presentation.exception_handlers import register_exception_handlers
from app.presentation.web.router import web_router

# Получаем настройки приложения
settings = get_settings()

# Определяем базовые пути
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "presentation" / "templates"
STATIC_DIR = BASE_DIR / "presentation" / "static"

# Создаем экземпляр шаблонизатора
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Менеджер контекста для жизненного цикла приложения."""
    # Startup
    log_info("Приложение запущено", environment=settings.ENVIRONMENT)
    # Создаем таблицы в базе данных
    await create_tables()
    yield
    # Shutdown
    if container:
        await container.close()
    log_info("Приложение остановлено")


# Создаем приложение FastAPI
app = FastAPI(
    title="User Management API",
    description="API для управления пользователями",
    version="1.0.0",
    lifespan=lifespan,
)

# Настраиваем Dishka для FastAPI
setup_dishka(container, app)

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Регистрируем статические файлы
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Регистрируем обработчики исключений
register_exception_handlers(app)

# Регистрируем API роутеры
app.include_router(api_public_router)
app.include_router(api_private_router)

# Регистрируем веб-роутеры для HTML страниц
app.include_router(web_router)


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
        "cookieAuth": {"type": "apiKey", "in": "cookie", "name": "access_token"}
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


@app.get("/health", response_class=HTMLResponse)
async def health_check(request: Request):
    """Проверка работоспособности API."""
    log_info("Запрос проверки работоспособности API")
    return templates.TemplateResponse("index.html", {"request": request})
