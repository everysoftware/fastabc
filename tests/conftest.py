from typing import AsyncGenerator

import pytest

from tests.connection import async_engine, async_session
from tests.models import Base
from tests.repositories import UserRepository


@pytest.fixture
async def user_repo() -> AsyncGenerator[UserRepository, None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield UserRepository(session)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
