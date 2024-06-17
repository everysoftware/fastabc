from typing import Any, Sequence

from pydantic import BaseModel

from onepattern import Page, PageParams
from onepattern.types import ModelData
from tests.schemas import UserRead


def validate_user(
    user: UserRead | None, data: ModelData, strict: bool = False
) -> None:
    assert user is not None

    if isinstance(data, BaseModel):
        data = data.model_dump()

    assert user.id is not None
    assert user.name == data["name"]
    assert user.age == data["age"]
    assert user.salary == data["salary"]
    assert user.created_at is not None
    assert user.updated_at is not None

    if strict:
        assert user.id == data["id"]
        assert user.updated_at == data["updated_at"]
        assert user.created_at == data["created_at"]


def validate_users(
    users: Page[UserRead], data: Sequence[ModelData], strict: bool = False
) -> None:
    assert users.total == len(users.items)
    assert users.total == len(data)
    for user, user_data in zip(users.items, data):
        validate_user(user, user_data, strict=strict)


def user_key(user: UserRead, params: PageParams) -> tuple[Any, ...]:
    keys = []
    for i in params.order_by:
        attr = getattr(user, i.field)
        if i.order == "desc":
            attr = -attr
        keys.append(attr)
    return tuple(keys)
