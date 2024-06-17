from sqlalchemy.orm import Mapped

from onepattern import AlchemyEntity


class UserAlchemyEntity(AlchemyEntity):
    __tablename__ = "users"

    name: Mapped[str]
    age: Mapped[int]
    salary: Mapped[int]
    # id, created_at and updated_at are added automatically
