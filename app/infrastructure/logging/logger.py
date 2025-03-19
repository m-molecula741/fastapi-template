"""Простой логгер для всего приложения."""
import logging
import sys
from datetime import datetime

# Создаем и настраиваем логгер
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# Создаем обработчик для вывода в консоль
handler = logging.StreamHandler(sys.stdout)

# Настраиваем формат логов
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.handlers = [handler]

# Отключаем логи от SQLAlchemy и других библиотек
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("passlib").setLevel(logging.ERROR)
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("fastapi").setLevel(logging.WARNING) 