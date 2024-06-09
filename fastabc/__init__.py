"""Ready-made API Abstractions: basic models, repositories, unit of work and other stuff."""

__version__ = "0.1.0"

from .alchemy import SkeletonBase, MixinBase, AlchemyEntity
from .schemas import SkeletonModel, MixinModel, Page, PageParams, EntityModel

__all__ = [
    "SkeletonModel",
    "SkeletonBase",
    "MixinModel",
    "MixinBase",
    "Page",
    "PageParams",
    "AlchemyEntity",
    "EntityModel",
]
