# Шаблон FastAPI проекта на чистой архитектуре

![Python](https://img.shields.io/badge/python-3.13.2+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.11+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.39+-yellow.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-2.10.6+-orange.svg)
![Dishka](https://img.shields.io/badge/Dishka-1.4.2+-purple.svg)

Этот проект представляет собой шаблон веб-приложения, построенного с использованием принципов чистой архитектуры (Clean Architecture).

## Содержание

- [Шаблон FastAPI проекта на чистой архитектуре](#шаблон-fastapi-проекта-на-чистой-архитектуре)
  - [Содержание](#содержание)
  - [Архитектура проекта](#архитектура-проекта)
    - [Преимущества чистой архитектуры](#преимущества-чистой-архитектуры)
    - [Слои архитектуры](#слои-архитектуры)
  - [Структура проекта](#структура-проекта)
  - [Основные функции](#основные-функции)
  - [API Endpoints](#api-endpoints)
    - [Публичные эндпоинты](#публичные-эндпоинты)
    - [Приватные эндпоинты (требуют авторизации)](#приватные-эндпоинты-требуют-авторизации)
  - [Установка и запуск](#установка-и-запуск)
    - [Требования](#требования)
    - [Установка зависимостей](#установка-зависимостей)
    - [Настройка окружения](#настройка-окружения)
    - [Запуск](#запуск)
  - [Тестирование](#тестирование)
  - [Миграции базы данных](#миграции-базы-данных)
  - [Линтинг и форматирование](#линтинг-и-форматирование)
  - [Особенности реализации](#особенности-реализации)
    - [Использование Dishka](#использование-dishka)
    - [Допущения](#допущения)

## Архитектура проекта

Проект следует принципам чистой архитектуры, которая разделяет код на несколько слоев:

### Преимущества чистой архитектуры

1. **Независимость от фреймворков** — архитектура не зависит от наличия каких-либо библиотек или фреймворков.
2. **Тестируемость** — бизнес-правила могут быть протестированы без UI, базы данных или любых внешних элементов.
3. **Независимость от UI** — UI можно легко изменить, не меняя остальную систему.
4. **Независимость от БД** — бизнес-правила не связаны с базой данных, поэтому можно легко заменить PostgreSQL на MongoDB или любую другую БД.
5. **Независимость от внешних агентов** — бизнес-правила ничего не знают о внешнем мире.

### Слои архитектуры

1. **Domain** — бизнес-сущности, интерфейсы репозиториев, исключения.
2. **Application** — сценарии использования (Use Cases) приложения.
3. **Infrastructure** — реализация репозиториев, работа с БД, внешние сервисы.
4. **Presentation** — API интерфейсы, обработчики запросов, роутеры.

## Структура проекта

```
app/
├── application/
│   └── use_cases/  # Use Cases приложения
│       ├── auth/   # Авторизация и работа с токенами
│       └── users/  # Работа с пользователями
├── domain/         # Доменный слой
│   ├── entities/   # Бизнес-сущности
│   ├── exceptions/ # Доменные исключения
│   └── interfaces/ # Интерфейсы репозиториев и сервисов
├── infrastructure/ # Инфраструктурный слой
│   ├── config/     # Конфигурация приложения
│   ├── database/   # Работа с базой данных
│   │   ├── models/ # ORM модели
│   │   └── repositories/ # Реализации репозиториев
│   ├── di/         # Внедрение зависимостей (Dishka)
│   ├── logging/    # Логирование
│   └── services/   # Реализации сервисов
└── presentation/   # Представительский слой
    ├── api/        # API эндпоинты
    │   ├── private/ # Приватные эндпоинты (требуют авторизации)
    │   └── public/  # Публичные эндпоинты
    └── schemas/    # Pydantic модели для валидации запросов/ответов

migrations/        # Миграции базы данных
tests/             # Тесты
```

## Основные функции

- **Регистрация и авторизация пользователей**
- **Управление токенами доступа и обновления**
- **Обновление токенов**
- **Выход из системы**
- **Веб-интерфейс для работы с API**

## API Endpoints

### Публичные эндпоинты

- **POST /api/users/register** - Регистрация нового пользователя
- **POST /api/auth/login** - Авторизация пользователя
- **PATCH /api/auth/refresh** - Обновление токенов

### Приватные эндпоинты (требуют авторизации)

- **DELETE /api/auth/logout** - Выход из системы (удаление сессии)
- **GET  /api/users/me** - Получение текущего пользователя

## Установка и запуск

### Требования

- Python 3.13.2+
- PostgreSQL

### Установка зависимостей

```bash
# С использованием uv
make install
```

### Настройка окружения

1. Создайте файл `.env` в корне проекта
2. Заполните его необходимыми переменными окружения:

```
.env.example -> .env
```

### Запуск

```bash
make run
```

Приложение будет доступно по адресу http://localhost:8000

## Тестирование

Проект содержит юнит-тесты для обеспечения качества кода:

```bash
# Запуск всех тестов
make test

# Запуск тестов с подробным выводом
make pytest
```

## Миграции базы данных

Управление схемой базы данных осуществляется с помощью Alembic:

```bash
# Создание новой миграции
make alembic-revision message="Migration description"

# Применение миграций
make alembic-upgrade

# Откат миграций
make alembic-downgrade steps=1
```

## Линтинг и форматирование

Проект использует современные инструменты для обеспечения качества кода:

```bash
# Проверка кода линтером
make lint

# Автоматическое форматирование кода
make format
```

## Особенности реализации

В проекте реализованы следующие архитектурные и технические решения:

1. **Чистая архитектура** — строгое разделение ответственности между слоями.
2. **Unit of Work и Repository** — для работы с данными.
3. **JWT-аутентификация** — для безопасной авторизации пользователей.
4. **Внедрение зависимостей с Dishka** — прозрачное управление зависимостями.
   - Прозрачное внедрение зависимостей через провайдеры
   - Автоматическое управление жизненным циклом зависимостей
   - Интеграция с FastAPI через `FromDishka[]`
   - Поддержка тестирования с заменой зависимостей моками
5. **Веб-интерфейс с Bootstrap 5** — современный адаптивный UI для работы с API.
   - Использование компонентов Bootstrap 5
   - Динамическое взаимодействие с API через JavaScript
   - Обработка JWT токенов и автоматическое обновление
   - Валидация форм на клиентской стороне
6. **Использование доменных сущностей во всех слоях** — для оптимизации производительности:
   - Доменные сущности используются напрямую во всех слоях приложения
   - Минимизация маппингов между слоями
   - Ускорение работы за счет отсутствия преобразований данных
   - Сохранение целостности бизнес-правил на всех уровнях

### Использование Dishka

Dishka используется для организации системы внедрения зависимостей (DI), что позволяет:

1. **Централизованно управлять зависимостями** через провайдеры:
   - `AppProvider` - общие зависимости приложения (настройки, БД, сервисы)
   - `UseCaseProvider` - провайдеры для use cases
   - `HttpProvider` - получение текущего юзера

2. **Упростить тестирование** за счет легкой замены настоящих компонентов моками:
   ```python
   # Пример использования в тестах
   login_usecase = LoginUseCase(mock_uow, mock_token_service)
   ```

3. **Улучшить типизацию** в API-эндпоинтах:
   ```python
   @router.post(
    "/register", response_model=UserCreateResp, status_code=status.HTTP_201_CREATED
   )
   @inject
   async def create_user(
      user_data: UserCreate,
      register_usecase: FromDishka[RegisterUserUseCase],
   ) -> UserCreateResp:
       # ...
   ```

4. **Автоматически управлять жизненным циклом** ресурсов с разными областями видимости:
   - `Scope.APP` - одиночные экземпляры на все приложение
   - `Scope.REQUEST` - новый экземпляр для каждого запроса

5. **Соблюдать принципы чистой архитектуры**, так как зависимости внедряются на уровне инфраструктуры и представления, не нарушая слои домена и приложения.

Контейнер настраивается при запуске приложения:
```python
def setup_container(app: FastAPI) -> Container:
    container = Container()
    container.register_provider(AppProvider())
    container.register_provider(UseCaseProvider())
    container.register_provider(HTTPProvider())
    setup_dishka(app, container)
    return container
```

### Допущения

В рамках шаблона было решено отказаться от DTO и использовать доменные сущности

1. **Уменьшение количества маппингов** - маппинги только между Pydantic и доменными сущностями: Request -> Domain, Domain -> Response
2. **Производительность** — маппинги больших струтур занимают много времени.
3. **Уменьшение количество кода** — отсутсвтие избыточного кода.