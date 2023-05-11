import yahooquery
from domain.asset.asset import Asset
from domain.exceptions import InvalidTicker


class AssetFactory:
    def make_new(self, ticker: str, units: int = 0) -> Asset:
        t = yahooquery.Ticker(ticker)

        profile = t.summary_profile[ticker]

        if type(profile) not in [dict]:
            raise InvalidTicker(f"Invalid ticker {ticker}")

        name = self.__extract_name(profile)

        country = profile["country"]
        sector = profile["sector"]
        return Asset(
            ticker=ticker,
            nr=units,
            name=name,
            country=country,
            sector=sector,
        )

    @classmethod
    def __extract_name(cls, profile: dict) -> str:
        summary = profile["longBusinessSummary"]
        words = summary.split(" ")
        first_2_words = words[0:2]
        name = " ".join(first_2_words)
        return name
