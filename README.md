# FastAPI Abstractions

Ready-made FastAPI abstractions: repository, unit of work, service etc.

## Features

- **Focus on business logic**: No need to write boilerplate code.
- **Scalable**: You can use the provided abstractions and easily extend them.
- **Portable**: Works with any database supported by SQLAlchemy.
- **Intuitive**: Great editor support. Completion everywhere. Less time debugging.
- **Easy**: Designed to be easy to use and learn. Less time reading docs.
- **Asynchronous**: Built-in support for async/await.
- **Use anywhere**: Use it with FastAPI, Aiogram, or any other framework (best with FastAPI).

## Requirements

FastAPI Abstractions stands on the shoulders of giants:

- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)

## Installation

```bash
pip install fastabc
```

## Concepts

* [Models](#1-models)
* [Repositories](#2-repositories)
* [Unit of Work](#3-unit-of-work)
* [Services](#4-services)
* [Use Cases](#5-use-cases)

## 1. Models

```python
from datetime import datetime

from sqlalchemy import Identity
from sqlalchemy.orm import Mapped, mapped_column

from fastabc import DeclarativeBase, AlchemyEntity
from fastabc.alchemy import SoftDeletable, HasID, HasTimestamp


# Classic way
class User(DeclarativeBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )


# Using AlchemyEntity
class UserAlchemyEntity(AlchemyEntity):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    # These columns will be added automatically
    # id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    # created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    # updated_at: Mapped[datetime] = mapped_column(
    #     default=datetime.now, onupdate=datetime.now
    # )


# Using mixins
class UserMixins(HasID, HasTimestamp, SoftDeletable):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    # These columns will be added automatically
    # id: Mapped[int]
    # created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    # updated_at: Mapped[datetime] = mapped_column(
    #     default=datetime.now, onupdate=datetime.now
    # )
    # deleted_at: Mapped[datetime | None] = None
```

## 2. Repositories

```python
from fastabc import AlchemyRepository
from .models import User


class UserRepository(AlchemyRepository[User]):
    model_type = User

```

## 3. Unit of Work

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from fastabc import AlchemyUOW
from .repositories import UserRepository


class UOW(AlchemyUOW):
    users: UserRepository

    async def on_open(self) -> None:
        self.users = UserRepository(self.session)


async_engine = create_async_engine("sqlite+aiosqlite:///memory")
async_session = async_sessionmaker(async_engine)

uow = UOW(async_session)
```

## 4. Services

```python
from fastabc import AlchemyService
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
        return await self.uow.users.get_many(where=[User.email.like(f"%@{domain}")])

    # And more...
```

## 5. Use Cases

```python
from faker import Faker

from .models import User
from .service import UserService
from .uow import uow

fake = Faker()


def get_users(domains: list[str], number: int = 10) -> list[User]:
    users = [User(email=fake.email(domain=domain), password=fake.password()) for _ in range(number) for domain in
             domains]
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
```

**Made with love ❤️**
