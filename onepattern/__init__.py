"""Scalable data access patterns for rapid API development, using SQLAlchemy & Pydantic."""

__version__ = "0.1.9"

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
