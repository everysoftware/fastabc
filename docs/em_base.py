from datetime import datetime

from sqlalchemy import Identity
from sqlalchemy.orm import Mapped, mapped_column

from onepattern import AlchemyBase


class UserAlchemyBase(AlchemyBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    salary: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )
