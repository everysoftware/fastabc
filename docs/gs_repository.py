from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from docs.gs_models import User, UserRead
from onepattern import AlchemyRepository


class UserRepository(AlchemyRepository[User, UserRead]):
    model_type = User
    schema_type = UserRead


async_engine = create_async_engine("sqlite+aiosqlite://", echo=True)
async_session = async_sessionmaker(async_engine)


async def get_user_repo() -> AsyncGenerator[UserRepository, None]:
    async with async_session() as session:
        async with session.begin():
            yield UserRepository(session)


UserRepoDep = Annotated[UserRepository, Depends(get_user_repo)]
