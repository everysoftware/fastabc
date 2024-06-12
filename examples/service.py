from onepattern import AlchemyService
from .models import User
from .uow import UOW


class UserService(AlchemyService):
    uow: UOW

    async def create(self, email: str, password: str) -> User:
        user = User(email=email, password=password)
        self.uow.users.add(user)
        await self.uow.commit()

        return user

    async def get(self, user_id: int) -> User | None:
        return await self.uow.users.get(user_id)

    async def get_by_email(self, email: str) -> User | None:
        return await self.uow.users.get_by_where(where=[User.email == email])

    async def create_many(self, users: list[User]) -> list[User]:
        await self.uow.users.insert(*users)
        await self.uow.commit()

        return users

    async def get_by_domain(self, domain: str) -> list[User]:
        return await self.uow.users.get_many(
            where=[User.email.like(f"%@{domain}")]
        )

    # And more...
