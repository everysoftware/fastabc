import datetime
from typing import Any, overload, Iterable

from pydantic import BaseModel
from sqlalchemy import inspect

from onepattern.schemas import Page
from onepattern.types import Model, Schema, ModelData, T


def naive_utc() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC).replace(tzinfo=None)


def to_dict(obj: ModelData | None) -> dict[str, Any]:
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    elif isinstance(obj, dict):
        return obj
    elif obj is None:
        return {}
    raise ValueError(f"Cannot convert {obj} (type: {type(obj)}) to dict")


def update_attrs(obj: T, data: ModelData | None = None, **attrs: Any) -> T:
    if isinstance(data, BaseModel):
        obj_dict = data.model_dump(exclude_unset=True)
    elif isinstance(data, dict):
        obj_dict = data
    else:
        raise ValueError(
            f"Cannot update {obj} with {data} (type: {type(data)})"
        )
    obj_dict |= attrs
    for name, value in obj_dict.items():
        setattr(obj, name, value)
    return obj


@overload
def instance_validate(instance: Model, schema_type: type[Schema]) -> Schema:
    ...


@overload
def instance_validate(
    instance: Model | None, schema_type: type[Schema]
) -> Schema | None:
    ...


def instance_validate(
    instance: Model | None, schema_type: type[Schema]
) -> Schema | None:
    if instance is None:
        return None
    return schema_type.model_validate(instance)


def instance_dump(instance: Model) -> dict[str, Any]:
    return {
        c.key: getattr(instance, c.key)
        for c in inspect(instance).mapper.column_attrs
    }


def make_page(
    instances: Iterable[Model], item_model: type[Schema]
) -> Page[Schema]:
    items = [item_model.model_validate(instance) for instance in instances]
    return Page[Schema](items=items)
