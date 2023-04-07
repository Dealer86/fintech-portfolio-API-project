from uuid import UUID

from domain.asset.asset import Asset


class User:
    def __init__(self, uuid: UUID, username: str, stocks: list[Asset] = None):
        self.__id = uuid
        self.__username = username
        self.__stocks = stocks if stocks else []

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def username(self) -> str:
        return self.__username

    @property
    def stocks(self) -> list[Asset]:
        return self.__stocks

    def add_stock(self, stock: Asset):
        self.__stocks.append(stock)
