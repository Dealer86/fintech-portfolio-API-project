import unittest
import uuid

from domain.asset.asset import Asset
from domain.user.user import User


class UserTestCase(unittest.TestCase):
    def test_user_sets_the_right_username(self):
        # set up
        username = "random-generated"
        id_ = uuid.uuid4()
        user = User(id_, username)
        # execution
        actual_username = user.username
        # assertion
        self.assertEqual(username, actual_username)

    def test_it_sets_empty_list_if_we_do_not_specify_stock(self):
        id_ = uuid.uuid4()
        username = "random-username"
        user = User(id_, username)

        actual_stocks = user.stocks

        self.assertEqual([], actual_stocks)

    def test_it_sets_the_stocks_we_give(self):
        id_ = uuid.uuid4()
        username = "random-name"

        actual_asset = [
            Asset(country="romania", ticker="aapl", nr=0, name="Apple", sector="Tech")
        ]

        user = User(id_, username, actual_asset)

        actual = user.stocks

        self.assertEqual(actual_asset, actual)

    def test_it_sets_the_id(self):
        id_ = uuid.uuid4()
        user1 = User(id_, "random-user")

        actual_id_user1 = user1.id

        self.assertEqual(actual_id_user1, id_)


if __name__ == "__main__":
    unittest.main()
