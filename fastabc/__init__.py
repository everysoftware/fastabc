"""Ready-made FastAPI abstractions: repository, unit of work, service etc."""

__version__ = "0.1.8"

from .alchemy import (
    DeclarativeBase,
    AlchemyMixin,
    AlchemyEntity,
    AlchemyUOW,
    AlchemyRepository,
    AlchemyService,
)
from .schemas import MixinModel, Page, PageParams, EntityModel

__all__ = [
    "DeclarativeBase",
    "MixinModel",
    "AlchemyMixin",
    "Page",
    "PageParams",
    "AlchemyEntity",
    "EntityModel",
    "AlchemyRepository",
    "AlchemyUOW",
    "AlchemyService",
]
