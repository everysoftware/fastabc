from datetime import datetime

from sqlalchemy import Identity
from sqlalchemy.orm import Mapped, mapped_column

from onepattern import DeclarativeBase, AlchemyEntity
from onepattern.alchemy import SoftDeletable, HasID, HasTimestamp


# Classic way
class User(DeclarativeBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )


# Using AlchemyEntity
class UserAlchemyEntity(AlchemyEntity):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    # These columns will be added automatically
    # id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    # created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    # updated_at: Mapped[datetime] = mapped_column(
    #     default=datetime.now, onupdate=datetime.now
    # )


# Using mixins
class UserMixins(HasID, HasTimestamp, SoftDeletable):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    # These columns will be added automatically
    # id: Mapped[int]
    # created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    # updated_at: Mapped[datetime] = mapped_column(
    #     default=datetime.now, onupdate=datetime.now
    # )
    # deleted_at: Mapped[datetime | None] = None
