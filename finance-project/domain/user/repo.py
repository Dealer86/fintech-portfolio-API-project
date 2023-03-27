from domain.user.user import User
import json


class UserRepo:
    def __init__(self, file_path: str):
        self.file_path = file_path
        try:
            with open(self.file_path) as f:
                contents = f.read()
            users_info = json.loads(contents)
            self.__users = [User(x) for x in users_info]
        except:
            self.__users = []

    def add(self, new_user: User):
        self.__users.append(new_user)
        users_info = [(x.id, x.username) for x in self.__users]
        users_json = json.dumps(users_info)
        with open(self.file_path, "w") as f:
            f.write(users_json)

    def get_all(self) -> list[User]:
        return self.__users

    def get_by_id(self, id_: str) -> User:
        for u in self.__users:
            if u.id == id_:
                return u

    def delete_by_id(self, id_: str):
        with open(self.file_path) as f:
            data = json.load(f)

        for i in range(len(data)):
            if data[i][0] == id_:
                del data[i]
                break

        with open(self.file_path, "w") as f:
            json.dump(data, f)

        self.__users = [u for u in self.__users if u.id != id_]
        return self.__users
