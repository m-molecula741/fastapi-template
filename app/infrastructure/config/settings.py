from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Настройки приложения, загружаемые из переменных окружения."""
    # Базовые настройки приложения
    APP_NAME: str = "FastAPI Template"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Настройки базы данных
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_DB: str = Field(default="template")
    
    # Настройки безопасности
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Настройки логирования
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    # Настройки токенов
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    @property
    def pg_db_creds(self) -> str:
        """Формируем строку с кредами"""
        return f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"

    @property
    def db_url(self) -> str:
        """DSN c параметрами подключения к БД"""
        url = (
            f"postgresql+asyncpg://"
            f"{self.pg_db_creds}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

        return url
    
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = ["development", "testing", "production"]
        if v.lower() not in allowed:
            raise ValueError(f"ENVIRONMENT должен быть одним из {allowed}")
        return v.lower()
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True
    }


def get_settings() -> Settings:
    """Возвращает экземпляр настроек приложения."""
    return Settings()
