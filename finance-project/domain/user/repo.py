from domain.user.user import User
import json


class UserRepo:
    def __init__(self, file_path: str):
        self.file_path = file_path
        try:
            file = open(file_path)
            contents = file.read()
            file.close()
            users_info = json.loads(contents)
            self.__users = [User(x) for x in users_info]
        except:
            self.__users = []

    def add(self, new_user: User):
        self.__users.append(new_user)
        users_info = [x.username for x in self.__users]
        users_json = json.dumps(users_info)
        # TODO Homework refactor with
        file = open(self.file_path, "w")
        file.write(users_json)
        file.close()

    def get_all(self) -> list[User]:
        return self.__users

    def get_by_username(self, username) -> User:
        for u in self.__users:
            if u.username == username:
                return u
