"""Ready-made FastAPI abstractions: repository, unit of work, service etc."""

__version__ = "0.1.7"

from .alchemy import (
    DeclarativeBase,
    MixinBase,
    AlchemyEntity,
    AlchemyUOW,
    AlchemyRepository,
    AlchemyService,
)
from .schemas import MixinModel, Page, PageParams, EntityModel

__all__ = [
    "DeclarativeBase",
    "MixinModel",
    "MixinBase",
    "Page",
    "PageParams",
    "AlchemyEntity",
    "EntityModel",
    "AlchemyRepository",
    "AlchemyUOW",
    "AlchemyService",
]
