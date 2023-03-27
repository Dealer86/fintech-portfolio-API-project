import unittest

from domain.user.user import User


class UserMyTestCase(unittest.TestCase):
    def test_user_sets_the_right_username(self):
        # set up
        username = "random-generated"
        user = User(username)
        # execution
        actual_username = user.username
        # assertion
        self.assertEqual(username, actual_username)

    def test_it_sets_empty_list_if_we_do_not_specify_stock(self):
        user = User("random-username")

        actual_stocks = user.stocks

        self.assertEqual([], actual_stocks)

    def test_it_sets_the_stocks_we_give(self):
        username = "random-name"
        stock_list = ["first", "second", "third"]

        user = User(username, stock_list)

        actual = user.stocks

        self.assertEqual(stock_list, actual)

    def test_it_sets_the_id(self):
        user1 = User("random-user1")
        user2 = User("random-user2")

        actual_id_user1 = user1.id
        actual_id_user2 = user2.id

        self.assertIsNotNone(actual_id_user1)
        self.assertIsNotNone(actual_id_user2)

        self.assertNotEqual(actual_id_user1, actual_id_user2)


if __name__ == "__main__":
    unittest.main()
