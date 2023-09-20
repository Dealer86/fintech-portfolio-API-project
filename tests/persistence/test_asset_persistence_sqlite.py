import sqlite3
import unittest

from domain.asset.asset import Asset
from domain.user.factory import UserFactory
from persistence.asset_sqlite import AssetPersistenceSqlite
from persistence.users_sqlite import UserPersistenceSqlite


class TestAssetPersistenceSqlite(unittest.TestCase):
    def setUp(self):
        self.asset_persistence_sqlite = AssetPersistenceSqlite()
        self.user_repo_sqlite = UserPersistenceSqlite()
        self.new_asset = Asset("aapl", 1, "Apple", "USA", "Tech")

    def test_get_for_user_if_list_is_empty(self):
        new_user = UserFactory.make_new("new-username1")

        self.user_repo_sqlite.add(new_user)
        asset_for_user = self.asset_persistence_sqlite.get_for_user(new_user)

        self.assertEqual([], asset_for_user)

    def test_add_to_user(self):
        new_user = UserFactory.make_new("new-username2")

        self.user_repo_sqlite.add(new_user)
        self.asset_persistence_sqlite.add_to_user(new_user, self.new_asset)

        user_asset = self.asset_persistence_sqlite.get_for_user(new_user)

        self.assertEqual(self.new_asset.ticker, user_asset[0].ticker)

    def test_get_for_user(self):
        new_user = UserFactory.make_new("new-username3")

        self.user_repo_sqlite.add(new_user)
        self.asset_persistence_sqlite.add_to_user(new_user, self.new_asset)

        user_asset = self.asset_persistence_sqlite.get_for_user(new_user)

        self.assertEqual(user_asset[0].ticker, self.new_asset.ticker)

    def test_delete_for_user(self):
        new_user = UserFactory.make_new("new-username4")

        self.user_repo_sqlite.add(new_user)
        self.asset_persistence_sqlite.add_to_user(new_user, self.new_asset)

        self.asset_persistence_sqlite.delete_for_user(
            str(new_user.id), self.new_asset.ticker
        )

        actual_user_assets = self.asset_persistence_sqlite.get_for_user(new_user)

        self.assertEqual([], actual_user_assets)

    @classmethod
    def tearDownClass(cls):
        # Clean up the data from all tables in the database
        db = sqlite3.connect("main_users.db")
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            cursor.execute(f"DELETE FROM '{table_name}';")

        db.commit()
        db.close()


if __name__ == "__main__":
    unittest.main()
