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
        await self.rollback()
        await self.close(type_, value, traceback)


class FakeUOW(AbstractUOW, ABC):
    _is_opened: bool = False

    @property
    def is_opened(self) -> bool:
        return self._is_opened

    async def open(self) -> None:
        self._is_opened = True
        await self.on_open()

    async def close(self, type_: Any, value: Any, traceback: Any) -> None:
        self._is_opened = False

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
