# Makefile для проекта

.PHONY: run test pytest alembic-revision alembic-upgrade clean install lint format

# Переменные
APP_MODULE = app.main:app
PORT = 8000
HOST = 127.0.0.1
ALEMBIC = alembic

# Запуск приложения
run:
	@echo "Запуск приложения на $(HOST):$(PORT)"
	uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT) --reload

# Запуск тестов
test:
	@echo "Запуск тестов"
	pytest

# Запуск тестов с более подробным выводом
pytest:
	@echo "Запуск тестов с подробным выводом"
	pytest -v

# Создание миграции Alembic
alembic-revision:
	@echo "Создание новой миграции"
	python cli.py make-migration -m "$(message)"

# Применение миграций
alembic-upgrade:
	@echo "Применение миграций"
	python cli.py migrate

# Откат миграций
alembic-downgrade:
	@echo "Откат миграций на $(steps) шагов"
	python cli.py rollback -n $(steps)

# Удаление временных файлов
clean:
	@echo "Удаление временных файлов"
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +

# Установка зависимостей с использованием uv
install:
	@echo "Установка зависимостей с использованием uv"
	uv pip install --no-deps -e .

# Запуск линтера ruff
lint:
	@echo "Запуск линтера ruff"
	ruff check app tests
	ruff format --check app tests

# Запуск форматирования кода
format:
	@echo "Форматирование кода"
	ruff format app tests
	ruff check --fix app tests --select I001
	black app tests
