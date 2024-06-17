from typing import Any, Final, TypeAlias

from faker import Faker

from tests.schemas import UserCreate

USER_COUNT: Final = 5
fake: Final = Faker()
UserModelData: TypeAlias = UserCreate | dict[str, Any]


def get_user_data() -> dict[str, Any]:
    user = {
        "name": fake.name(),
        "age": fake.random_int(1, 100),
        "salary": fake.random_int(1000, 10000),
    }
    return user


def get_users_data() -> list[dict[str, Any]]:
    return [get_user_data() for _ in range(USER_COUNT)]


def get_user() -> UserCreate:
    return UserCreate(**get_user_data())


def get_users() -> list[UserCreate]:
    return [get_user() for _ in range(USER_COUNT)]


def get_model_data(*, duplicates: bool = False) -> list[UserModelData]:
    preset: list[UserModelData] = [get_user_data(), get_user()]
    if duplicates:
        preset *= 2
    return preset


def get_model_data_many() -> list[list[UserModelData]]:
    return [
        get_users(),  # type: ignore[list-item]
        get_users_data(),  # type: ignore[list-item]
    ]
