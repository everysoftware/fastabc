from typing import Sequence

import pytest

from onepattern import PageParams, utils, exceptions
from onepattern.types import ModelData, WhereClause
from tests.faking import get_model_data, get_model_data_many, UserModelData
from tests.models import User
from tests.repositories import UserRepository
from tests.utils import validate_user, validate_users, user_key


@pytest.mark.parametrize(
    "data",
    get_model_data(),
)
async def test_create(user_repo: UserRepository, data: UserModelData) -> None:
    user = await user_repo.create(data)
    validate_user(user, data)


@pytest.mark.parametrize(
    "data",
    get_model_data(),
)
async def test_get(user_repo: UserRepository, data: ModelData) -> None:
    user = await user_repo.create(data)
    validate_user(await user_repo.get(user.id), data)


@pytest.mark.parametrize(
    "data",
    get_model_data(),
)
@pytest.mark.parametrize(
    "new_data",
    get_model_data(),
)
async def test_update(
    user_repo: UserRepository, data: ModelData, new_data: ModelData
) -> None:
    user = await user_repo.create(data)
    user = await user_repo.update(user.id, new_data)
    validate_user(user, new_data)


@pytest.mark.parametrize(
    "data",
    get_model_data(),
)
async def test_delete(user_repo: UserRepository, data: ModelData) -> None:
    expected = await user_repo.create(data)
    user = await user_repo.delete(expected.id)
    validate_user(user, expected)

    assert await user_repo.get(expected.id) is None


async def test_get_not_existing(
    user_repo: UserRepository,
) -> None:
    assert await user_repo.get(1) is None


async def test_get_one_not_existing(
    user_repo: UserRepository,
) -> None:
    with pytest.raises(exceptions.OPNoResultFound):
        await user_repo.get_one(1)


async def test_update_not_existing(
    user_repo: UserRepository,
) -> None:
    with pytest.raises(exceptions.OPNoResultFound):
        await user_repo.update(1, {})


async def test_delete_not_existing(
    user_repo: UserRepository,
) -> None:
    with pytest.raises(exceptions.OPNoResultFound):
        await user_repo.delete(1)


@pytest.mark.parametrize(
    "data",
    get_model_data_many(),
)
async def test_create_many(
    user_repo: UserRepository, data: Sequence[ModelData]
) -> None:
    users = await user_repo.create_many(*data, ret=True, sort=True)
    validate_users(users, data)


@pytest.mark.parametrize(
    "data",
    get_model_data_many(),
)
@pytest.mark.parametrize(
    "limit, offset",
    [(i, j) for i in range(1, 6) for j in range(0, 5)],
)
async def test_get_many_limit_offset(
    user_repo: UserRepository,
    data: Sequence[ModelData],
    limit: int,
    offset: int,
) -> None:
    expected = await user_repo.create_many(*data, ret=True, sort=True)

    users = await user_repo.get_many(limit=limit, offset=offset)
    validate_users(users, expected.items[offset : offset + limit], strict=True)  # noqa: E203


@pytest.mark.parametrize(
    "data",
    get_model_data_many(),
)
@pytest.mark.parametrize(
    "params",
    [
        PageParams(limit=4, offset=0, sort="salary:asc,age:asc"),
        PageParams(limit=3, offset=0, sort="salary:desc,age:desc"),
        PageParams(limit=2, offset=0, sort="salary:asc,age:desc"),
        PageParams(limit=1, offset=0, sort="salary:desc,age:asc"),
    ],
)
async def test_get_many_params(
    user_repo: UserRepository, data: Sequence[ModelData], params: PageParams
) -> None:
    expected = await user_repo.create_many(*data, ret=True, sort=True)
    expected.items.sort(key=lambda x: user_key(x, params))

    users = await user_repo.get_many(params=params)
    validate_users(
        users,
        expected.items[params.offset : params.offset + params.limit],  # noqa: E203
        strict=True,
    )


@pytest.mark.parametrize(
    "data",
    get_model_data(),
)
async def test_get_by_where(
    user_repo: UserRepository, data: ModelData
) -> None:
    expected = await user_repo.create(data)
    user = await user_repo.get_by_where(User.name == expected.name)
    validate_user(user, expected)


@pytest.mark.parametrize(
    "where",
    [
        User.name == "John",
    ],
)
async def test_get_by_where_not_existing(
    user_repo: UserRepository, where: WhereClause
) -> None:
    user = await user_repo.get_by_where(where)
    assert user is None


@pytest.mark.parametrize("data", [get_model_data(duplicates=True)])
async def test_get_by_where_multiple_results(
    user_repo: UserRepository, data: Sequence[ModelData]
) -> None:
    await user_repo.create_many(*data)
    double_name = (
        data[0]["name"] if isinstance(data[0], dict) else data[0].name  # type: ignore[attr-defined]
    )
    with pytest.raises(exceptions.OPMultipleResultsFound):
        await user_repo.get_by_where(User.name == double_name)


@pytest.mark.parametrize(
    "where",
    [
        User.name == "John",
    ],
)
async def test_get_one_by_where_not_existing(
    user_repo: UserRepository, where: WhereClause
) -> None:
    with pytest.raises(exceptions.OPNoResultFound):
        await user_repo.get_one_by_where(where)


@pytest.mark.parametrize(
    "data",
    get_model_data_many(),
)
@pytest.mark.parametrize(
    "new_data",
    get_model_data_many(),
)
async def test_update_many(
    user_repo: UserRepository,
    data: Sequence[ModelData],
    new_data: Sequence[ModelData],
) -> None:
    users = await user_repo.create_many(*data, ret=True, sort=True)
    update_data = users.items
    for user, update in zip(update_data, new_data):
        utils.update_attrs(user, update)

    await user_repo.update_many(*update_data)
    result = await user_repo.get_many()
    validate_users(result, new_data)


@pytest.mark.parametrize(
    "data",
    get_model_data_many(),
)
async def test_delete_many(
    user_repo: UserRepository,
    data: Sequence[ModelData],
) -> None:
    expected = await user_repo.create_many(*data, ret=True, sort=True)
    users = await user_repo.delete_many(
        [i.id for i in expected.items], ret=True
    )

    validate_users(users, expected.items)

    result = await user_repo.get_many()
    assert result.total == 0


@pytest.mark.parametrize(
    "data",
    get_model_data_many(),
)
async def test_delete_many_by_where(
    user_repo: UserRepository,
    data: Sequence[ModelData],
) -> None:
    expected = await user_repo.create_many(*data, ret=True, sort=True)
    users = await user_repo.delete_many(
        where=[User.id.in_(i.id for i in expected.items)], ret=True
    )

    validate_users(users, expected.items)

    result = await user_repo.get_many()
    assert result.total == 0


@pytest.mark.parametrize(
    "data",
    get_model_data_many(),
)
async def test_delete_many_negative(
    user_repo: UserRepository,
    data: Sequence[ModelData],
) -> None:
    with pytest.raises(exceptions.OPValueError):
        await user_repo.delete_many(
            idents=[1], where=[User.age == 42], ret=True
        )
    with pytest.raises(exceptions.OPValueError):
        await user_repo.delete_many()
