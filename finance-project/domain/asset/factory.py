import yahooquery
from domain.asset.asset import Asset
from domain.exceptions import InvalidTicker
import logging


class AssetFactory:
    def make_new(self, ticker: str) -> Asset:
        logging.info(f"Asset Factory executing create_new command for ticker {ticker}")
        t = yahooquery.Ticker(ticker)

        profile = t.summary_profile[ticker]

        if type(profile) not in [dict]:
            raise InvalidTicker(f"Invalid ticker {ticker}")

        name = self.__extract_name(profile)

        country = profile["country"]
        sector = profile["sector"]
        logging.info(
            f"Asset Factory successfully executed create_new command for ticker {ticker}"
        )
        return Asset(
            ticker=ticker,
            nr=0,
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

    @classmethod
    def from_tuple(cls, info: tuple) -> Asset:
        return Asset(
            ticker=info[0], nr=info[1], name=info[2], country=info[3], sector=info[4]
        )
