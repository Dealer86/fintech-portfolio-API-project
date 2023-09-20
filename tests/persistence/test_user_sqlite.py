import sqlite3
import unittest

from domain.user.factory import UserFactory
from persistence.users_sqlite import UserPersistenceSqlite


class TestUserPersistenceSqlite(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.persistence = UserPersistenceSqlite()

    def test_add(self):
        # set up
        user = UserFactory.make_new("test-username")

        # execution
        self.persistence.add(user)
        all_users = self.persistence.get_all()

        # assertion
        self.assertEqual(len(all_users), 1)

    def test_delete(self):
        # set up
        user = UserFactory.make_new("test-username")
        self.persistence.add(user)

        # execution
        self.persistence.delete(str(user.id))
        all_id_from_database = [str(u.id) for u in self.persistence.get_all()]

        # assertion
        self.assertNotIn(str(user.id), all_id_from_database)

    def test_update(self):
        # set up
        user = UserFactory.make_new("test-username")
        self.persistence.add(user)

        user_id = str(user.id)
        expected_username = "updated-username"

        # execution
        self.persistence.update(user_id, expected_username)
        all_username_from_database = [u.username for u in self.persistence.get_all()]

        # assertion
        self.assertIn(expected_username, all_username_from_database)

    def test_get_all(self):
        # set up
        user = UserFactory.make_new("test-username")
        user2 = UserFactory.make_new("test-username2")
        user_list = [user, user2]

        for every_user in user_list:
            self.persistence.add(every_user)

        # execution
        actual_users = self.persistence.get_all()

        # assertion
        self.assertEqual(len(actual_users), 3)

    @classmethod
    def tearDownClass(cls) -> None:
        import sqlite3

        with sqlite3.connect("main_users.db") as db:
            cursor = db.cursor()
            cursor.execute("DROP TABLE users")
            db.commit()


if __name__ == "__main__":
    unittest.main()
