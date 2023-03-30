from domain.user.factory import UserFactory
from domain.user.user import User
import json


class UserRepo:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.__load()

    def add(self, new_user: User):
        self.__users.append(new_user)
        users_info = [(str(x.id), x.username, x.stocks) for x in self.__users]
        users_json = json.dumps(users_info)
        with open(self.file_path, "w") as f:
            f.write(users_json)

    def get_all(self) -> list[User]:
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



    def __load(self):
        try:
            with open(self.file_path) as f:
                contents = f.read()
            users_info = json.loads(contents)
            factory = UserFactory()
            self.__users = [factory.make_from_persistence(x) for x in users_info]
        except:
            # TODO thursday logging
            self.__users = []

