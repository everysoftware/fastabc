import pytest

from tests.faking import get_users
from tests.models import User
from tests.repositories import UserRepository
from tests.schemas import UserCreate


@pytest.mark.parametrize(
    "data",
    [get_users()],
)
async def test_sum(user_repo: UserRepository, data: list[UserCreate]) -> None:
    await user_repo.create_many(*data)
    expected_sum = sum(u.salary for u in data)
    assert await user_repo.sum(User.salary) == expected_sum


@pytest.mark.parametrize(
    "data",
    [get_users()],
)
async def test_count(
    user_repo: UserRepository, data: list[UserCreate]
) -> None:
    await user_repo.create_many(*data)
    assert await user_repo.count() == len(data)


@pytest.mark.parametrize(
    "data",
    [get_users()],
)
async def test_avg(user_repo: UserRepository, data: list[UserCreate]) -> None:
    await user_repo.create_many(*data)
    expected_sum = sum(u.salary for u in data)
    assert await user_repo.avg(User.salary) == expected_sum / len(data)


@pytest.mark.parametrize(
    "data",
    [get_users()],
)
async def test_max(user_repo: UserRepository, data: list[UserCreate]) -> None:
    await user_repo.create_many(*data)
    expected_max = max(u.salary for u in data)
    assert await user_repo.max(User.salary) == expected_max


@pytest.mark.parametrize(
    "data",
    [get_users()],
)
async def test_min(user_repo: UserRepository, data: list[UserCreate]) -> None:
    await user_repo.create_many(*data)
    expected_min = min(u.salary for u in data)
    assert await user_repo.min(User.salary) == expected_min
