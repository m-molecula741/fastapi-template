"""Базовый класс для use cases."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# Тип результата
T = TypeVar("T")


class UseCase(Generic[T], ABC):
    """Базовый класс для всех use cases."""

    @abstractmethod
    async def execute(self, *args, **kwargs) -> T:
        """Выполняет use case."""
        pass
