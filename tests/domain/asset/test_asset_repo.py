import unittest

from domain.asset.factory import AssetFactory
from domain.asset.repo import AssetRepo
from domain.user.factory import UserFactory
from persistence.asset_file import AssetPersistenceFile
from persistence.user_file import UserPersistenceFile


class AssetRepoCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.users_file = "main_users.json"

        cls.user_persistence = UserPersistenceFile(cls.users_file)

        cls.asset_persistence = AssetPersistenceFile(cls.users_file)
        cls.repo = AssetRepo(cls.asset_persistence)

    def test_it_add_to_user(self):
        # set up
        new_username = "random-username"
        user_factory = UserFactory()
        new_user = user_factory.make_new(new_username)
        self.user_persistence.add(new_user)

        new_ticker = "aapl"
        asset_factory = AssetFactory()
        actual_asset = asset_factory.make_new(new_ticker)

        # execution
        self.repo.add_to_user(new_user, actual_asset)

        expected_asset_list = self.repo.get_for_user(new_user)
        expected_asset = [
            u.ticker for u in expected_asset_list if u.ticker == new_ticker
        ]

        # assertion
        self.assertIn(actual_asset.ticker, expected_asset)

    def test_it_delete_for_user(self):
        # set up
        new_username = "random-username2"
        user_factory = UserFactory()
        new_user = user_factory.make_new(new_username)
        self.user_persistence.add(new_user)

        new_ticker = "tsla"
        asset_factory = AssetFactory()
        actual_asset = asset_factory.make_new(new_ticker)

        self.repo.add_to_user(new_user, actual_asset)

        # execution
        self.repo.delete_for_user(str(new_user.id), actual_asset.ticker)

        # assertion
        expected_asset = [
            u.ticker for u in self.asset_persistence.get_for_user(new_user)
        ]

        self.assertNotIn(actual_asset.ticker, expected_asset)

    def test_it_gets_for_user(self):
        # set up
        new_username = "random-username3"
        user_factory = UserFactory()
        new_user = user_factory.make_new(new_username)
        self.user_persistence.add(new_user)

        new_ticker = "adi"
        asset_factory = AssetFactory()
        actual_asset = asset_factory.make_new(new_ticker)

        self.repo.add_to_user(new_user, actual_asset)

        # execution
        asset_list = self.repo.get_for_user(new_user)
        asset_ticker_list = [a.ticker for a in asset_list]
        self.assertIn(actual_asset.ticker, asset_ticker_list)

    @classmethod
    def tearDown(cls):
        import os

        os.remove("main_users.json")


if __name__ == "__main__":
    unittest.main()
