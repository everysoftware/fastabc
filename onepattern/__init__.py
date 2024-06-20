"""One pattern for accessing data powered by SQLAlchemy & Pydantic."""

__version__ = "0.2.2"

from .models import (
    AlchemyBase,
    AlchemyMixin,
    AlchemyEntity,
)
from .repository import AlchemyRepository
from .schemas import MixinModel, Page, PageParams, EntityModel
from .uow import AbstractUOW, AlchemyUOW, MultipleAlchemyUOW, FakeUOW

__all__ = [
    "AlchemyBase",
    "MixinModel",
    "AlchemyMixin",
    "Page",
    "PageParams",
    "AlchemyEntity",
    "EntityModel",
    "AlchemyRepository",
    "AlchemyUOW",
    "MultipleAlchemyUOW",
    "AbstractUOW",
    "FakeUOW",
]
