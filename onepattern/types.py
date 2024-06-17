from typing import Sequence, Any, TypeVar, TypeAlias, ParamSpec

from pydantic import BaseModel
from sqlalchemy import BinaryExpression, ColumnElement, UnaryExpression
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T")
P = ParamSpec("P")
Model = TypeVar("Model", bound=DeclarativeBase)
Schema = TypeVar("Schema", bound=BaseModel)

ModelData = BaseModel | dict[str, Any]
ID: TypeAlias = Any | tuple[Any, ...]
WhereClause: TypeAlias = BinaryExpression[bool] | ColumnElement[bool]
WhereClauseSeq: TypeAlias = Sequence[WhereClause]
OrderBy: TypeAlias = UnaryExpression[Any] | ColumnElement[Any]
OrderBySeq: TypeAlias = Sequence[OrderBy]
Column: TypeAlias = ColumnElement[Any]
ColumnSeq: TypeAlias = Sequence[Column]
