import uuid
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

    @username.setter
    def username(self, new_username):
        self.__username = new_username

    @property
    def stocks(self) -> list[Asset]:
        return self.__stocks

    def to_tuple(self) -> tuple:
        asset_tuple = [a.to_tuple() for a in self.stocks]
        print(asset_tuple)
        return str(self.id), self.__username, asset_tuple


