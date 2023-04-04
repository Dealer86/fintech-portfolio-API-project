from domain.user.factory import UserFactory
from domain.user.persistance_interface import UserPersistenceInterface
from domain.user.user import User
import json


class UserRepo:
    def __init__(self, persistence: UserPersistenceInterface):
        self.__persistence = persistence
        self.__users = None

    def add(self, new_user: User):
        # TODO homework, refactor to not have duplicate code + add for get_by_id
        if self.__users is None:
            self.__users = self.__persistence.get_all()
        self.__users.append(new_user)
        self.__persistence.add(new_user)

    def get_all(self) -> list[User]:
        if self.__users is None:
            self.__users = self.__persistence.get_all()
        return self.__users

    def get_by_id(self, id_: str) -> User:
        for u in self.__users:
            if str(u.id) == id_:
                return u

    def delete_by_id(self, id_: str):
        self.__users = [u for u in self.__users if str(u.id) != id_]

        with open(self.file_path) as f:
            content = f.read()
        users_info = json.loads(content)

        for every_user in users_info:
            if every_user[0] == id_:
                users_info.remove(every_user)

        with open(self.file_path, "w") as f:
            json.dump(users_info, f)





