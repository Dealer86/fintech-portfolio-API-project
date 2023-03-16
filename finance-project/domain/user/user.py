class User:
    def __init__(self, username: str, stocks: list[str] = None):
        self.__username = username
        self.__stocks = stocks if stocks else []

    @property
    def username(self) -> str:
        return self.__username

    @property
    def stocks(self) -> list[str]:
        return self.__stocks
