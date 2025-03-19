"""Простой логгер для всего приложения."""
import logging
import os
import sys
from datetime import datetime

# Создаем директорию для логов если она не существует
os.makedirs("logs", exist_ok=True)

# Создаем и настраиваем логгер
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
logger.propagate = False  # Предотвращает дублирование логов

# Очищаем существующие обработчики если они есть
if logger.handlers:
    logger.handlers.clear()

# Создаем обработчик для вывода в консоль
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Создаем обработчик для вывода в файл
file_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)

# Настраиваем формат логов
log_format = "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Отключаем логи от SQLAlchemy и других библиотек
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("passlib").setLevel(logging.ERROR)
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("fastapi").setLevel(logging.WARNING)

# Функции-обертки для удобного структурированного логирования

def log_error(message: str, error=None, **kwargs):
    """Логирует ошибку с контекстом."""
    error_message = f"{message}"
    if error:
        error_message = f"{message}: {str(error)}"
    
    context = " | ".join([f"{k}={v}" for k, v in kwargs.items()]) if kwargs else ""
    if context:
        error_message = f"{error_message} | {context}"
    
    logger.error(error_message)

def log_info(message: str, **kwargs):
    """Логирует информационное сообщение с контекстом."""
    context = " | ".join([f"{k}={v}" for k, v in kwargs.items()]) if kwargs else ""
    if context:
        message = f"{message} | {context}"
    
    logger.info(message)

def log_warning(message: str, **kwargs):
    """Логирует предупреждение с контекстом."""
    context = " | ".join([f"{k}={v}" for k, v in kwargs.items()]) if kwargs else ""
    if context:
        message = f"{message} | {context}"
    
    logger.warning(message) 