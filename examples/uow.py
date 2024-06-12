from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from onepattern import AlchemyUOW
from .repositories import UserRepository


class UOW(AlchemyUOW):
    users: UserRepository

    async def on_open(self) -> None:
        self.users = UserRepository(self.session)


async_engine = create_async_engine("sqlite+aiosqlite:///memory")
async_session = async_sessionmaker(async_engine)

uow = UOW(async_session)
