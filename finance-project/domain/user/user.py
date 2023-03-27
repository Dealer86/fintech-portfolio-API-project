import uuid


class User:
    def __init__(self, username: str, stocks: list[str] = None, id_: str = None):
        self.__username = username
        self.__stocks = stocks if stocks else []
        self.__id_ = id_ if id_ is not None else str(uuid.uuid4())

    @property
    def username(self) -> str:
        return self.__username

    @property
    def stocks(self) -> list[str]:
        return self.__stocks

    @property
    def id(self):
        return self.__id_
