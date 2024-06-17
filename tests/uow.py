from onepattern import AlchemyUOW
from .connection import async_session
from .repositories import UserRepository


class UOW(AlchemyUOW):
    users: UserRepository

    async def on_open(self) -> None:
        self.users = UserRepository(self.session)


uow = UOW(async_session)
