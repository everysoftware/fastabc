from sqlalchemy.orm import Mapped

from .mixins import AlchemyEntity


class TestUser(AlchemyEntity):
    __tablename__ = "__test_users__"

    name: Mapped[str]
    age: Mapped[int]
