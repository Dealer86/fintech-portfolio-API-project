import unittest
import os

from domain.asset.asset import Asset
from domain.user.factory import UserFactory


from persistence.asset_file import AssetPersistenceFile
from persistence.user_file import UserPersistenceFile


class TestAssetPersistenceFile(unittest.TestCase):
    def setUp(self):
        self.filename = "test_data.json"
        self.asset_persistence = AssetPersistenceFile(self.filename)
        self.user_repo = UserPersistenceFile(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_get_all_empty_file(self):
        users = self.asset_persistence.get_all()
        self.assertEqual(len(users), 0)

    def test_add_to_user(self):
        user = UserFactory.make_new("John-Doe")

        asset = Asset("AAPL", 10, "Apple", "Us", "tech")

        self.user_repo.add(user)

        self.asset_persistence.add_to_user(user, asset)

        users = self.asset_persistence.get_all()

        self.assertEqual(len(users), 1)
        self.assertEqual(len(users[0].stocks), 1)
        self.assertEqual(users[0].stocks[0].ticker, "AAPL")
        self.assertEqual(users[0].stocks[0].units, 10)

    def test_delete_for_user(self):
        user = UserFactory.make_new("John-Doe")

        asset1 = Asset("AAPL", 10, "Apple", "Us", "tech")
        asset2 = Asset("GOOGL", 5, "Google", "New York", "tech")

        self.user_repo.add(user)

        self.asset_persistence.add_to_user(user, asset1)
        self.asset_persistence.add_to_user(user, asset2)

        self.asset_persistence.delete_for_user(str(user.id), "AAPL")

        users = self.asset_persistence.get_all()

        self.assertEqual(len(users), 1)
        self.assertEqual(len(users[0].stocks), 1)
        self.assertEqual(users[0].stocks[0].ticker, "GOOGL")
        self.assertEqual(users[0].stocks[0].units, 5)

    def test_get_for_user(self):
        user1 = UserFactory.make_new("John-Doe")

        asset1 = Asset("AAPL", 10, "Apple", "Us", "tech")

        self.user_repo.add(user1)

        self.asset_persistence.add_to_user(user1, asset1)

        user1_assets = self.asset_persistence.get_for_user(user1)

        self.assertEqual(len(user1_assets), 1)
        self.assertEqual(user1_assets[0].ticker, "AAPL")
        self.assertEqual(user1_assets[0].units, 10)


if __name__ == "__main__":
    unittest.main()
