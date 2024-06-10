from fastabc import AlchemyRepository
from .models import User


class UserRepository(AlchemyRepository[User]):
    model_type = User
