from __future__ import annotations

from typing import Generic, TypeVar, Literal, cast

from pydantic import Field, computed_field, BaseModel

OrderType = Literal["asc", "desc"]


class OrderByItem(BaseModel):
    field: str
    order: OrderType = "asc"

    @classmethod
    def from_str(cls, value: str) -> OrderByItem:
        values = value.lower().split(":")
        if len(values) == 1:
            return OrderByItem(field=values[0])
        if len(values) == 2 and values[1] in ["asc", "desc"]:
            return OrderByItem(
                field=values[0], order=cast(OrderType, values[1])
            )
        raise ValueError(f"Invalid order by item: {value}")


class PageParams(BaseModel):
    limit: int = Field(10, ge=0, le=100)
    offset: int = Field(0, ge=0)
    sort: str = "updated_at:desc"

    @computed_field  # type: ignore[misc]
    @property
    def order_by(self) -> list[OrderByItem]:
        sort = self.sort.split(",")
        return [OrderByItem.from_str(i) for i in sort]


Model = TypeVar("Model", bound=BaseModel)


class Page(BaseModel, Generic[Model]):
    items: list[Model]

    @computed_field  # type: ignore[misc]
    @property
    def total(self) -> int:
        return len(self.items)
