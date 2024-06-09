from fastabc.abc import AbstractService
from fastabc.alchemy import AlchemyUOW


class AlchemyService(AbstractService):
    uow: AlchemyUOW

    def __init__(self, uow: AlchemyUOW):
        self.uow = uow
