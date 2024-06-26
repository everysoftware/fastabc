from __future__ import annotations

from typing import Any, cast

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    AsyncSessionTransaction,
)

from .abstract import AbstractUOW


class AlchemyUOW(AbstractUOW):
    """
    SQLAlchemy UOW.

    Usage::

        class UOW(AlchemyUOW):
            users: UserRepository

            async def on_open(self) -> None:
                self.users = UserRepository(self.session)


        async with UOW(session_factory) as uow:
            # TRANSACTION IS BEGUN...

            await uow.users.create(User(name="Bob", age="18"))

    """  # noqa: E501

    factory: async_sessionmaker[AsyncSession]
    session: AsyncSession
    transaction: AsyncSessionTransaction

    def __init__(self, factory: async_sessionmaker[AsyncSession]):
        self.factory = factory

    @property
    def is_opened(self) -> bool:
        if not self.session:
            return False

        return cast(bool, self.session.is_active)

    async def on_open(self) -> None:
        ...

    async def open(self) -> None:
        self.session = self.factory()
        await self.session.__aenter__()
        self.transaction = self.session.begin()
        await self.transaction.__aenter__()
        await self.on_open()

    async def close(self, type_: Any, value: Any, traceback: Any) -> None:
        await self.transaction.__aexit__(type_, value, traceback)
        await self.session.__aexit__(type_, value, traceback)

    async def flush(self) -> None:
        await self.session.flush()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def commit(self) -> None:
        await self.session.commit()
