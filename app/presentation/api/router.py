"""Основной роутер для API."""
from fastapi import APIRouter

from app.presentation.api.public.users import router as users_router
from app.presentation.api.public.auth import router as auth_router
from app.presentation.api.private.users import router as users_private_router
from app.presentation.api.private.auth import router as auth_private_router

api_private_router = APIRouter(prefix="/api/private")
api_public_router = APIRouter(prefix="/api/public")


api_public_router.include_router(users_router, prefix="/users", tags=["users"]) 
api_public_router.include_router(auth_router, prefix="/auth", tags=["auth"])

api_private_router.include_router(users_private_router, prefix="/users", tags=["private users"])
api_private_router.include_router(auth_private_router, prefix="/auth", tags=["private auth"])