from onepattern import AlchemyRepository
from .models import User
from .schemas import UserRead


class UserRepository(AlchemyRepository[User, UserRead]):
    model_type = User
    schema_type = UserRead
