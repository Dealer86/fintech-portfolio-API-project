import unittest
from unittest.mock import patch, MagicMock
from domain.asset.asset import Asset
from domain.asset.factory import AssetFactory
from domain.exceptions import InvalidTicker


class TestAssetFactory(unittest.TestCase):
    @patch("yahooquery.Ticker")
    def test_make_new_with_valid_ticker(self, mock_yahoo_ticker):
        mock_profile = {
            "country": "US",
            "sector": "Technology",
            "longBusinessSummary": "Apple Inc. designs, manufactures, and markets smartphones,"
            " personal computers, tablets, wearables, and accessories worldwide.",
        }
        mock_yahoo_ticker_instance = MagicMock()
        mock_yahoo_ticker_instance.summary_profile = {"AAPL": mock_profile}
        mock_yahoo_ticker.return_value = mock_yahoo_ticker_instance

        asset_factory = AssetFactory()
        asset = asset_factory.make_new("AAPL")

        self.assertIsInstance(asset, Asset)
        self.assertEqual(asset.ticker, "AAPL")
        self.assertEqual(asset.units, 0)
        self.assertEqual(asset.name, "Apple Inc.")
        self.assertEqual(asset.country, "US")
        self.assertEqual(asset.sector, "Technology")

    @patch("yahooquery.Ticker")
    def test_make_new_with_invalid_ticker(self, mock_yahoo_ticker):
        mock_yahoo_ticker_instance = MagicMock()
        mock_yahoo_ticker_instance.summary_profile = {"not_a_valid_invalid": None}
        mock_yahoo_ticker.return_value = mock_yahoo_ticker_instance

        asset_factory = AssetFactory()

        with self.assertRaises(InvalidTicker) as context:
            asset_factory.make_new("not_a_valid_invalid")

        self.assertEqual("Invalid ticker not_a_valid_invalid", str(context.exception))
