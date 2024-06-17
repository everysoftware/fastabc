from contextlib import asynccontextmanager
from typing import Annotated, Any

from fastapi import FastAPI, Depends, HTTPException

from docs.gs_models import Base, UserCreate, UserRead
from docs.gs_repository import async_engine, UserRepoDep
from onepattern import PageParams, Page


@asynccontextmanager
async def lifespan(_app: FastAPI) -> Any:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/users/")
async def create_user(user: UserCreate, users: UserRepoDep) -> UserRead:
    return await users.create(user)


async def get_user_dep(user_id: int, users: UserRepoDep) -> UserRead:
    user = await users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/{user_id}")
async def get_user(
    user: Annotated[UserRead, Depends(get_user_dep)],
) -> UserRead:
    return user


@app.put("/users/{user_id}")
async def update_user(
    update: UserCreate,
    user: Annotated[UserRead, Depends(get_user_dep)],
    users: UserRepoDep,
) -> UserRead:
    return await users.update(user.id, update)


@app.delete("/users/{user_id}")
async def delete_user(
    user: Annotated[UserRead, Depends(get_user_dep)],
    users: UserRepoDep,
) -> UserRead:
    return await users.delete(user.id)


@app.get("/users/")
async def get_users(
    params: Annotated[PageParams, Depends()],
    users: UserRepoDep,
) -> Page[UserRead]:
    return await users.get_many(params=params)
