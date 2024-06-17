from typing import Any

from .abstract import AbstractUOW


class FakeUOW(AbstractUOW):
    """Unit of work that does nothing."""

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
