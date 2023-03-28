import unittest

from domain.user.factory import UserFactory
from domain.user.repo import UserRepo


class UserRepoTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.users_file = "test_users.json"
        cls.repo = UserRepo(cls.users_file)

    def test_it_adds_a_user(self):
        expected_username = "a-username"
        new_user = UserFactory().make_new(expected_username)

        self.repo.add(new_user)

        actual_users = self.repo.get_all()
        self.assertEqual(1, len(actual_users))
        self.assertEqual(expected_username, actual_users[0].username)

    def test_it_reads_a_user_from_the_system(self):
        repo = UserRepo(self.users_file)

        actual_users = repo.get_all()
        self.assertEqual(1, len(actual_users))

    # TODO homework
    @unittest.skip
    def test_it_deletes_a_user_from_system(self):
        pass


if __name__ == "__main__":
    unittest.main()
