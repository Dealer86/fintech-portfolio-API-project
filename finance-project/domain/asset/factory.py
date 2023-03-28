import yahooquery
from domain.asset.asset import Asset


class AssetFactory:
    def make_new(self, ticker: str) -> Asset:
        # TODO error handling & tests
        t = yahooquery.Ticker(ticker)
        profile = t.summary_profile[ticker]
        name = profile["longBusinessSummary"].split(" ")[0:2]
        country = profile["country"]
        sector = profile["sector"]
        return Asset(
            ticker=ticker,
            nr=0,
            name=name,
            country=country,
            sector=sector,
        )
