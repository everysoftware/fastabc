from sqlalchemy.orm import DeclarativeBase, Mapped

from onepattern.models import HasID, HasTimestamp


class Base(DeclarativeBase):
    pass


class UserMixins(Base, HasID, HasTimestamp):
    __tablename__ = "users"

    name: Mapped[str]
    age: Mapped[int]
    salary: Mapped[int]
