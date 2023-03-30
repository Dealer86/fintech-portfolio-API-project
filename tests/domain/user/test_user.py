import unittest
import uuid
from domain.user.user import User


class UserMyTestCase(unittest.TestCase):
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
        stock_list = ["first", "second", "third"]

        user = User(id_, username, stock_list)

        actual = user.stocks

        self.assertEqual(stock_list, actual)

    def test_it_sets_the_id(self):
        id_ = uuid.uuid4()
        user1 = User(id_, "random-user1")

        actual_id_user1 = user1.id

        self.assertIsNotNone(actual_id_user1)

        self.assertIsInstance(actual_id_user1, type(id_))

    def test_id_consistency(self):
        # create two User objects with different UUIDs
        id1 = uuid.uuid4()
        id2 = uuid.uuid4()
        user1 = User(id1, 'test_user1')
        user2 = User(id2, 'test_user2')

        # check that both users have different ids
        self.assertNotEqual(user1.id, user2.id)


if __name__ == "__main__":
    unittest.main()
