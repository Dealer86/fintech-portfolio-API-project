import sqlite3
import unittest

from domain.user.factory import UserFactory
from persistence.users_sqlite import UserPersistenceSqlite


class TestUserPersistenceSqlite(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.persistence = UserPersistenceSqlite()
        cls.factory = UserFactory()

    def test_add(self):
        # set up
        user = self.factory.make_new("test-username")

        # execution
        self.persistence.add(user)
        all_users = self.persistence.get_all()

        # assertion
        self.assertEqual(len(all_users), 1)

        # clean up
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM users WHERE id = '{str(user.id)}'")
            conn.commit()

    def test_delete(self):
        # set up
        user = self.factory.make_new("test-username")
        self.persistence.add(user)

        # execution
        self.persistence.delete(str(user.id))
        all_id_from_database = [str(u.id) for u in self.persistence.get_all()]

        # assertion
        self.assertNotIn(str(user.id), all_id_from_database)

    def test_update(self):
        # set up
        user = self.factory.make_new("test-username")
        self.persistence.add(user)

        user_id = str(user.id)
        expected_username = "updated-username"

        # execution
        self.persistence.update(user_id, expected_username)
        all_username_from_database = [u.username for u in self.persistence.get_all()]

        # assertion
        self.assertIn(expected_username, all_username_from_database)

        # clean up
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM users WHERE id='{str(user.id)}'")
            conn.commit()

    def test_get_all(self):
        # set up
        user = self.factory.make_new("test-username")
        user2 = self.factory.make_new("test-username2")
        user_list = [user, user2]

        for every_user in user_list:
            self.persistence.add(every_user)

        # execution
        actual_users = self.persistence.get_all()

        # assertion
        self.assertEqual(len(actual_users), 2)

        # clean up
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            # cursor.execute(f"DELETE FROM users WHERE id='{str(user.id)}'")
            # cursor.execute(f"DELETE FROM users WHERE id='{str(user2.id)}'")
            cursor.execute("DROP TABLE users")
            conn.commit()

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     import os
    #     os.remove("main_users.db")


if __name__ == "__main__":
    unittest.main()
