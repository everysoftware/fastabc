from onepattern.interfaces import AbstractService
from onepattern.alchemy import AlchemyUOW


class AlchemyService(AbstractService):
    uow: AlchemyUOW

    def __init__(self, uow: AlchemyUOW):
        self.uow = uow
