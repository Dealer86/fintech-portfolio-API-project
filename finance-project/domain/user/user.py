from uuid import UUID


class User:
    def __init__(self, uuid: UUID, username: str, stocks: list[str] = None):
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
    def stocks(self) -> list[str]:
        return self.__stocks
