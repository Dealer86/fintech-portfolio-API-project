import unittest

from domain.user.factory import UserFactory
from domain.user.repo import UserRepo
from persistence.asset_file import AssetPersistenceFile
from persistence.user_file import UserPersistenceFile


class UserRepoTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.users_file = "test_users.json"
        cls.assets_file = "test_users.json"
        cls.persistence = UserPersistenceFile(cls.users_file)
        cls.asset_persistence = AssetPersistenceFile(cls.assets_file)
        cls.repo = UserRepo(cls.persistence, cls.asset_persistence)

    def test_it_deletes_a_user(self):
        expected_username = "test-username1"
        new_user = UserFactory().make_new(expected_username)

        self.repo.add(new_user)

        self.repo.delete(str(new_user.id))

        users_list = [str(u.id) for u in self.repo.get_all()]
        self.assertNotIn(str(new_user.id), users_list)

    def test_it_adds_a_user(self):
        expected_username = "test-username"
        new_user = UserFactory().make_new(expected_username)

        self.repo.add(new_user)

        actual_users = self.repo.get_all()

        self.assertEqual(1, len(actual_users))
        self.assertEqual(expected_username, actual_users[0].username)

    def test_it_edits_a_user(self):
        new_user = UserFactory().make_new("username-before")

        self.repo.add(new_user)

        self.repo.update(str(new_user.id), "updated-username")

        all_usernames = [x.username for x in self.repo.get_all()]

        self.assertIn("updated-username", all_usernames)

    def test_it_gets_a_user_by_id(self):
        expected_username = "test-username2"
        new_user = UserFactory().make_new(expected_username)

        self.repo.add(new_user)

        actual_user = self.repo.get_by_id(str(new_user.id))

        self.assertEqual(expected_username, actual_user.username)

    def test_it_gets_all_users(self):
        # execution
        actual_users = self.repo.get_all()
        # assertion
        self.assertEqual(len(self.repo.get_all()), 3)

    @classmethod
    def tearDownClass(cls) -> None:
        import os

        if os.path.exists("test_users.json"):
            os.remove("test_users.json")


if __name__ == "__main__":
    unittest.main()
