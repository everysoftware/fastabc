from abc import ABC, abstractmethod
from typing import Any, Self


class AbstractUOW(ABC):
    """Provides transaction management"""

    @property
    @abstractmethod
    def is_opened(self) -> bool:
        pass

    async def on_open(self) -> None:
        pass

    @abstractmethod
    async def open(self) -> None:
        pass

    @abstractmethod
    async def close(self, type_: Any, value: Any, traceback: Any) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass

    async def __aenter__(self) -> Self:
        await self.open()
        return self

    async def __aexit__(self, type_: Any, value: Any, traceback: Any) -> None:
        await self.close(type_, value, traceback)
