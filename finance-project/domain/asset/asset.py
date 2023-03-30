import yfinance


class Asset:
    def __init__(self, ticker: str, nr: float, name: str, country: str, sector: str):
        self.__ticker = ticker
        self.__nr = nr
        self.__name = name
        self.__country = country
        self.__sector = sector
        self.__yfin = yfinance.Ticker(ticker)

    @property
    def ticker(self) -> str:
        return self.__ticker

    @property
    def units(self) -> float:
        return self.__nr

    @property
    def name(self) -> str:
        return self.__name

    @property
    def country(self) -> str:
        return self.__country

    @property
    def current_price(self) -> float:
        price = self.__yfin.fast_info["lastPrice"]
        return round(price, 2)

    @property
    def currency(self) -> str:
        return self.__yfin.fast_info["currency"]

    @property
    def closed_price(self) -> float:
        return self.__yfin.fast_info["previousClose"]

    @property
    def fifty_day_price(self) -> float:
        return self.__yfin.fast_info["fiftyDayAverage"]

    #TODO a property, in percentage how much it went up or down
    # currentPrice & closed_price


