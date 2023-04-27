import os
import unittest

from domain.user.factory import UserFactory

from persistence.user_file import UserPersistenceFile


class UserPersistenceFileTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.users_file = "test_users.json"
        cls.repo = UserPersistenceFile(cls.users_file)

    def test_it_adds_a_user(self):
        expected_username = "a-username"
        new_user = UserFactory().make_new(expected_username)

        self.repo.add(new_user)

        actual_users = self.repo.get_all()
        self.assertEqual(1, len(actual_users))
        self.assertEqual(expected_username, actual_users[0].username)

    def test_it_reads_users_from_the_system(self):
        a_username = "a-username"
        new_user = UserFactory().make_new(a_username)

        self.repo.add(new_user)

        actual_users = self.repo.get_all()

        self.assertIsNotNone(actual_users)
        self.assertIn(new_user.username, actual_users[0].username)

    def test_it_deletes_a_user_from_system(self):
        a_username = "a-username"
        new_user = UserFactory().make_new(a_username)

        self.repo.add(new_user)

        self.repo.delete(str(new_user.id))

        all_id_from_system = [str(u.id) for u in self.repo.get_all()]
        self.assertNotIn(str(new_user.id), all_id_from_system)

    def test_it_gets_a_user_by_id_from_system(self):
        a_username = "a-username"
        new_user = UserFactory().make_new(a_username)
        expected_id = new_user.id

        self.repo.add(new_user)

        actual_user = self.repo.get_by_id(str(new_user.id))
        actual_id = actual_user.id

        self.assertEqual(expected_id, actual_id)

    def test_it_updates_a_users_username_to_system(self):
        a_username = "username-before"
        new_user = UserFactory().make_new(a_username)
        username_before_update = new_user.username

        self.repo.add(new_user)

        self.repo.update(str(new_user.id), "updated-username")
        actual_user = self.repo.get_by_id(str(new_user.id))
        username_after_update = actual_user.username

        self.assertNotEqual(username_before_update, username_after_update)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test_users.json")


if __name__ == "__main__":
    unittest.main()
