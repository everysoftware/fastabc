from faker import Faker

from .models import User
from .service import UserService
from .uow import uow

fake = Faker()


def get_users(domains: list[str], number: int = 10) -> list[User]:
    users = [
        User(email=fake.email(domain=domain), password=fake.password())
        for _ in range(number)
        for domain in domains
    ]
    return users


async def main():
    async with uow:
        service = UserService(uow)

        user = await service.create("user@example.com", "qwerty12345")
        print(user)

        user = await service.get(user.id)
        print(user)

        user = await service.get_by_email("user@example.com")
        print(user)

        users = get_users(["gmail.com", "yahoo.com"])
        await service.create_many(*users)

        users = await service.get_by_domain("gmail.com")
        print(users)
