"""Роутер для веб-страниц."""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Определяем базовые пути
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "presentation" / "templates"

# Создаем экземпляр шаблонизатора
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Создаем роутер
web_router = APIRouter(
    tags=["web"],
)


@web_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Главная страница."""
    return templates.TemplateResponse("index.html", {"request": request})


@web_router.get("/auth/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Страница входа."""
    return templates.TemplateResponse("auth/login.html", {"request": request})


@web_router.get("/auth/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Страница регистрации."""
    return templates.TemplateResponse("auth/register.html", {"request": request})


@web_router.get("/users/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    """Страница профиля пользователя."""
    return templates.TemplateResponse("users/profile.html", {"request": request})
