from typing import Generic, Sequence, cast, Iterable, overload, Literal, Any

import sqlalchemy.exc
from sqlalchemy import (
    select,
    func,
    insert,
    update,
    delete,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm.interfaces import ORMOption

from onepattern import utils
from onepattern.types import (
    WhereClauseSeq,
    OrderBySeq,
    Model,
    ID,
    T,
    Schema,
    ColumnSeq,
    WhereClause,
    ModelData,
)
from ..exceptions import OPNoResultFound, OPMultipleResultsFound, OPValueError
from ..schemas import PageParams, Page


class AlchemyRepository(Generic[Model, Schema]):
    """
    Repository for SQLAlchemy models.

    Usage::

        class UserRepository(AlchemyRepository[User, UserRead]):
            model_type = User


        users = UserRepository(session)
    """

    model_type: type[Model]
    schema_type: type[Schema]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, data: ModelData | None = None, **attrs: Any
    ) -> Schema:
        """
        Create an instance in the database ::

            user_create = UserCreate(name="Bob", age=20)
            user = await users.create(user_create)

        """  # noqa: E501
        instance = self.model_type(**utils.to_dict(data), **attrs)
        self.session.add(instance)
        await self.session.flush()
        return utils.instance_validate(instance, self.schema_type)

    async def get(
        self,
        ident: ID,
        *,
        options: Sequence[ORMOption] | None = None,
    ) -> Schema | None:
        """
        Get an instance by ID ::

            user = await users.get(1)

        """
        instance = await self.session.get(
            self.model_type, ident, options=options
        )
        return utils.instance_validate(instance, self.schema_type)

    async def get_one(
        self,
        ident: ID,
        *,
        options: Sequence[ORMOption] | None = None,
    ) -> Schema:
        """
        Get an instance by ID. Raise `NoResultFound` if not found ::

            user = await users.get_one(1)

        """
        response = await self.get(
            ident,
            options=options,
        )
        if response is None:
            raise OPNoResultFound()
        return response

    async def _get_many(
        self,
        *,
        where: WhereClauseSeq | None = None,
        group_by: ColumnSeq | None = None,
        having: WhereClauseSeq | None = None,
        distinct: ColumnSeq | None = None,
        order_by: OrderBySeq | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Model]:
        stmt = select(self.model_type)
        if where is not None:
            stmt = stmt.where(*where)
        if group_by is not None:
            stmt = stmt.group_by(*group_by)
        if having is not None:
            stmt = stmt.having(*having)
        if distinct is not None:
            stmt = stmt.distinct(*distinct)
        if order_by is not None:
            stmt = stmt.order_by(*order_by)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        result = await self.session.execute(stmt)
        instances = list(result.scalars().all())
        return instances

    async def get_many(
        self,
        *,
        params: PageParams | None = None,
        where: WhereClauseSeq | None = None,
        group_by: ColumnSeq | None = None,
        having: WhereClauseSeq | None = None,
        distinct: ColumnSeq | None = None,
        order_by: OrderBySeq | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Page[Schema]:
        """
        Paginate instances from the database ::

                response = await users.get_many(
                    PageParams(limit=10, offset=0, sort="created_at:asc"),
                    where=[User.age > 18],
                )

        """
        if params is not None:
            order_by = []
            for item in params.order_by:
                attr = getattr(self.model_type, item.field)
                order_by.append(
                    attr.asc() if item.order == "asc" else attr.desc()
                )
            limit = params.limit
            offset = params.offset
        instances = await self._get_many(
            where=where,
            group_by=group_by,
            having=having,
            distinct=distinct,
            order_by=order_by,
            limit=limit,
            offset=offset,
        )
        return utils.make_page(instances, self.schema_type)

    async def update(self, ident: ID, data: ModelData) -> Schema:
        """
        Update an instance in the database with given data ::

            response = await users.update(1, {"name": "Alice"})

        """  # noqa: E501
        try:
            instance = await self.session.get_one(self.model_type, ident)
        except sqlalchemy.exc.NoResultFound as e:
            raise OPNoResultFound from e
        utils.update_attrs(instance, data)
        await self.session.flush()
        return utils.instance_validate(instance, self.schema_type)

    async def delete(self, ident: ID, soft: bool = False) -> Schema:
        """
        Delete an instance from the database ::

            await users.delete(1)

        """
        try:
            instance = await self.session.get_one(self.model_type, ident)
        except sqlalchemy.exc.NoResultFound as e:
            raise OPNoResultFound from e
        if not soft:
            await self.session.delete(instance)
        else:
            instance.deleted_at = utils.naive_utc()  # type: ignore[attr-defined]
        await self.session.flush()
        return utils.instance_validate(instance, self.schema_type)

    async def get_by_where(
        self,
        *where: WhereClause,
    ) -> Schema | None:
        """
        Get instance from the database that meets the condition.

        Return `None` if not found.
        Raise `sqlalchemy.exc.MultipleResultsFound` if more than one found::

            response = await users.get_by_where(User.name == "Alice")

        """
        instances = await self._get_many(where=where, limit=2)
        if not instances:
            return None
        if len(instances) > 1:
            raise OPMultipleResultsFound()
        return utils.instance_validate(instances[0], self.schema_type)

    async def get_one_by_where(
        self,
        *where: WhereClause,
    ) -> Schema:
        """
        Get instance from the database that meets the condition.

        Raise `sqlalchemy.exc.NoResultFound` if not found.
        Raise `sqlalchemy.exc.MultipleResultsFound` if more than one found::

            response = await users.get_one_by_where(User.name == "Alice")
        """
        response = await self.get_by_where(*where)
        if not response:
            raise OPNoResultFound()
        return response

    @overload
    async def create_many(
        self,
        *data: ModelData,
        ret: Literal[True],
        sort: bool = False,
    ) -> Page[Schema]:
        ...

    @overload
    async def create_many(
        self,
        *data: ModelData,
        ret: Literal[False] = False,
    ) -> None:
        ...

    async def create_many(
        self,
        *data: ModelData,
        ret: bool = False,
        sort: bool = False,
    ) -> Page[Schema] | None:
        """
        Create many instances in the database ::

            users = [
                UserCreate(name="Alice", age=20),
                UserCreate(name="Bob", age=30),
            ]

            response = await users.create_many(*users, ret=True)

        """
        if not data:
            return None
        create_data = tuple(utils.to_dict(obj) for obj in data)
        stmt = insert(self.model_type)
        if ret:
            stmt = stmt.returning(
                self.model_type, sort_by_parameter_order=sort
            )
        result = await self.session.execute(stmt, create_data)
        if not ret:
            return None
        instances = result.scalars().all()
        return utils.make_page(instances, self.schema_type)

    @overload
    async def update_many(
        self,
        *data: ModelData,
        where: WhereClauseSeq | None = None,
        ret: Literal[True],
    ) -> Page[Schema]:
        ...

    @overload
    async def update_many(
        self,
        *data: ModelData,
        where: WhereClauseSeq | None = None,
        ret: Literal[False] = False,
    ) -> None:
        ...

    async def update_many(
        self,
        *data: ModelData,
        where: WhereClauseSeq | None = None,
        ret: bool = False,
    ) -> Page[Schema] | None:
        """
        Update many instances into the database ::

            users = [{"id": 1, "name": "Not Bob"}, {"id": 2, "name": "Not Alice"}]
            user_ids = await users.update_many(*users)

        """
        if not data:
            return None
        update_data = list(utils.to_dict(obj) for obj in data)
        stmt = update(self.model_type)
        if where:
            stmt = stmt.where(*where)
        if ret:
            stmt = stmt.returning(self.model_type)
        result = await self.session.execute(stmt, update_data)
        if not ret:
            return None
        instances = result.scalars().all()
        return utils.make_page(instances, self.schema_type)

    @overload
    async def delete_many(
        self,
        idents: Iterable[ID] | None = None,
        *,
        where: WhereClauseSeq | None = None,
        ret: Literal[True],
    ) -> Page[Schema]:
        ...

    @overload
    async def delete_many(
        self,
        idents: Iterable[ID] | None = None,
        *,
        where: WhereClauseSeq | None = None,
        ret: Literal[False] = False,
    ) -> None:
        ...

    async def delete_many(
        self,
        idents: Iterable[ID] | None = None,
        *,
        where: WhereClauseSeq | None = None,
        ret: bool = False,
    ) -> Page[Schema] | None:
        """
        Delete many instances from the database ::

            await users.delete_many([1, 2, 3])

        """
        if not idents and not where:
            raise OPValueError("Provide idents or where clause to delete_many")
        if idents and where:
            raise OPValueError("Provide idents or where clause, not both")
        if idents:
            where = [self.model_type.id.in_(idents)]  # type: ignore[attr-defined]
        stmt = delete(self.model_type)
        if where:
            stmt = stmt.where(*where)
        if ret:
            stmt = stmt.returning(self.model_type)  # type: ignore[assignment]
        result = await self.session.execute(stmt)
        if not ret:
            return None
        instances = result.scalars().all()
        return utils.make_page(instances, self.schema_type)

    async def avg(
        self,
        attribute: InstrumentedAttribute[T],
        where: WhereClauseSeq | None = None,
    ) -> T:
        """
        Get the average value of an attribute from the database.
        Raise `sqlalchemy.exc.NoResultFound` if no result ::

            avg_age = await users.avg(User.age, where=[User.age > 18])

        """
        stmt = select(func.avg(attribute))
        if where is not None:
            stmt = stmt.where(*where)
        result = await self.session.execute(stmt)
        scalar = cast(T, result.scalar_one())
        return scalar

    async def count(self, *where: WhereClauseSeq) -> int:
        """
        Count instances in the database that meets the condition.

            count = await users.count([User.age > 18])

        """
        stmt = select(func.count()).select_from(self.model_type)
        if where:
            stmt = stmt.where(*where)  # type: ignore[arg-type]
        result = await self.session.execute(stmt)
        scalar = result.scalar_one()
        return scalar

    async def max(
        self,
        attribute: InstrumentedAttribute[T],
        where: WhereClauseSeq | None = None,
    ) -> T:
        """
        Get the maximum value of an attribute from the database.
        Raise `sqlalchemy.exc.NoResultFound` if no result ::

            max_age = await users.max(User.age, where=[User.age < 45])
        """
        stmt = select(func.max(attribute))
        if where is not None:
            stmt = stmt.where(*where)
        result = await self.session.execute(stmt)
        scalar = result.scalar_one()
        return scalar

    async def min(
        self,
        attribute: InstrumentedAttribute[T],
        where: WhereClauseSeq | None = None,
    ) -> T:
        """
        Get the minimum value of an attribute from the database.
        Raise `sqlalchemy.exc.NoResultFound` if no result ::

            min_age = await users.min(User.age, where=[User.age > 18])
        """
        stmt = select(func.min(attribute))
        if where is not None:
            stmt = stmt.where(*where)
        result = await self.session.execute(stmt)
        scalar = result.scalar_one()
        return scalar

    async def sum(
        self,
        attribute: InstrumentedAttribute[T],
        where: WhereClauseSeq | None = None,
    ) -> T:
        """
        Get the sum of an attribute from the database.
        Raise `sqlalchemy.exc.NoResultFound` if no result ::

            salary_sum = await users.sum(User.salary, where=[User.age > 18])
        """
        stmt = select(func.sum(attribute))
        if where is not None:
            stmt = stmt.where(*where)
        result = await self.session.execute(stmt)
        scalar = result.scalar_one()
        return scalar
