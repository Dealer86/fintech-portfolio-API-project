import unittest

from domain.asset.asset import Asset

from domain.user.factory import UserFactory
from persistence.asset_file import AssetPersistenceFile


class AssetPersistenceFileTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.asset_file = "test_asset.json"
        cls.persistence_file = AssetPersistenceFile(cls.asset_file)
        cls.new_user = UserFactory.make_new("test-username")

    def test_it_adds_asset_to_user(self):
        new_user = self.new_user
        asset = Asset("aapl", 0, "Apple", "New York", "Tech")

        self.persistence_file.add_to_user(new_user, asset)

        actual_assets = self.persistence_file.get_for_user(new_user)

        self.assertIn(asset.ticker, actual_assets[0].ticker)

    def test_it_get_asset_for_user(self):
        pass


if __name__ == '__main__':
    unittest.main()
