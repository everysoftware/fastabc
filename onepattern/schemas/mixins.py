import datetime

from pydantic import Field, BaseModel


# https://docs.pydantic.dev/latest/concepts/models/#abstract-base-classes


class MixinModel(BaseModel):
    """Base class for all mixins."""


class HasID(MixinModel):
    id: int = Field(ge=1)


class HasTimestamp(MixinModel):
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
    )


class SoftDeletable(MixinModel):
    deleted_at: datetime.datetime | None = Field(
        None,
    )


class EntityModel(HasID, HasTimestamp):
    pass
