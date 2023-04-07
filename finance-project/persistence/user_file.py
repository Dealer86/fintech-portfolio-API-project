import json

from domain.user.factory import UserFactory
from domain.user.persistance_interface import UserPersistenceInterface
from domain.user.user import User


class UserPersistenceFile(UserPersistenceInterface):
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def get_all(self) -> list[User]:
        try:
            with open(self.__file_path) as f:
                contents = f.read()
            users_info = json.loads(contents)
            factory = UserFactory()
            return [factory.make_from_persistence(x) for x in users_info]
        except:
            # TODO Homework. log error
            return []

    def add(self, user: User):
        current_users = self.get_all()
        current_users.append(user)
        users_info = [(str(x.id), x.username, x.stocks) for x in current_users]
        users_json = json.dumps(users_info)
        with open(self.__file_path, "w") as f:
            f.write(users_json)
