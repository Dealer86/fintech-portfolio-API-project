import unittest

from unittest.mock import patch
from domain.asset.asset import Asset


class AssetTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.__asset = Asset("AAPL", 10, "Apple Inc.", "US", "Technology")

    def test_ticker(
        self,
    ):
        self.assertEqual(self.__asset.ticker, "AAPL")

    def test_nr(self):
        self.assertEqual(self.__asset.units, 10)

    def test_name(self):
        self.assertEqual(self.__asset.name, "Apple Inc.")

    def test_country(self):
        self.assertEqual(self.__asset.country, "US")

    def test_sector(self):
        self.assertEqual(self.__asset.sector, "Technology")

    @patch("yfinance.Ticker")
    def test_current_price(self, mock_yfinance):
        expected = 120.12
        mock_yfinance.return_value.fast_info = {"lastPrice": expected}
        asset = Asset("AAPL", 10, "Apple Inc.", "US", "Technology")
        self.assertEqual(asset.current_price, expected)

    @patch("yfinance.Ticker")
    def test_currency(self, mock_yfinance):
        expected = "USD"
        mock_yfinance.return_value.fast_info = {"currency": expected}
        asset = Asset("AAPL", 10, "Apple Inc.", "US", "Technology")
        self.assertEqual(asset.currency, expected)

    @patch("yfinance.Ticker")
    def test_today_low_price(self, mock_yfinance):
        expected = 99.12
        mock_yfinance.return_value.fast_info = {"dayLow": expected}
        asset = Asset("AAPL", 10, "Apple Inc.", "US", "Technology")
        self.assertEqual(asset.today_low_price, expected)

    @patch("yfinance.Ticker")
    def test_today_high_price(self, mock_yfinance):
        expected = 110.01
        mock_yfinance.return_value.fast_info = {"dayHigh": expected}
        asset = Asset("AAPL", 10, "Apple Inc.", "US", "Technology")
        self.assertEqual(asset.today_high_price, expected)

    @patch("yfinance.Ticker")
    def test_open_price(self, mock_yfinance):
        expected = 109.21
        mock_yfinance.return_value.fast_info = {"open": expected}
        asset = Asset("AAPL", 10, "Apple Inc.", "US", "Technology")
        self.assertEqual(asset.open_price, expected)

    @patch("yfinance.Ticker")
    def test_close_price(self, mock_yfinance):
        expected = 102.21
        mock_yfinance.return_value.fast_info = {"previousClose": expected}
        asset = Asset("AAPL", 10, "Apple Inc.", "US", "Technology")
        self.assertEqual(asset.closed_price, expected)

    @patch("yfinance.Ticker")
    def test_fifty_day_price(self, mock_yfinance):
        expected = 145.21
        mock_yfinance.return_value.fast_info = {"fiftyDayAverage": expected}
        asset = Asset("goog", 1, "Google", "US", "Tech")
        self.assertEqual(asset.fifty_day_price, expected)


if __name__ == "__main__":
    unittest.main()
