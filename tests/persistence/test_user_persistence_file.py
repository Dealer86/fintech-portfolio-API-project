import os
import unittest

from domain.user.factory import UserFactory

from persistence.user_file import UserPersistenceFile


class UserPersistenceFileTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.users_file = "test_users.json"
        cls.persistence_file = UserPersistenceFile(cls.users_file)

    def test_it_adds_a_user(self):
        expected_username = "a-username"
        new_user = UserFactory().make_new(expected_username)

        self.persistence_file.add(new_user)

        actual_users = self.persistence_file.get_all()
        self.assertEqual(1, len(actual_users))
        self.assertEqual(expected_username, actual_users[0].username)

    def test_it_reads_users_from_file(self):
        a_username = "a-username"
        new_user = UserFactory().make_new(a_username)

        self.persistence_file.add(new_user)

        actual_users = self.persistence_file.get_all()

        self.assertIsNotNone(actual_users)
        self.assertIn(new_user.username, actual_users[0].username)

    def test_it_deletes_a_user_from_file(self):
        a_username = "a-username"
        new_user = UserFactory().make_new(a_username)

        self.persistence_file.add(new_user)

        self.persistence_file.delete(str(new_user.id))

        all_id_from_system = [str(u.id) for u in self.persistence_file.get_all()]
        self.assertNotIn(str(new_user.id), all_id_from_system)

    def test_it_updates_a_username_to_file(self):
        new_user = UserFactory().make_new("username-before")

        self.persistence_file.add(new_user)

        self.persistence_file.update(str(new_user.id), "updated-username")

        all_usernames = [x.username for x in self.persistence_file.get_all()]

        self.assertIn("updated-username", all_usernames)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test_users.json")


if __name__ == "__main__":
    unittest.main()
