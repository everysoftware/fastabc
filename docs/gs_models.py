from datetime import datetime

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Identity
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    salary: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )


class UserBase(BaseModel):
    name: str
    age: int
    salary: int

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
