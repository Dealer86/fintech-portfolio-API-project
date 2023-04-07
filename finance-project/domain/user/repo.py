import uuid
import json

from domain.asset.repo import AssetRepo
from domain.user.factory import UserFactory
from domain.user.persistance_interface import UserPersistenceInterface
from domain.user.user import User


class UserRepo:
    def __init__(self, persistence: UserPersistenceInterface):
        self.__persistence = persistence
        self.__users = None

    def add(self, new_user: User):
        self.__persistence.add(new_user)
        self.__check_users_not_none()
        self.__users.append(new_user)

    def get_all(self) -> list[User]:
        self.__check_users_not_none()
        return self.__users

    def get_by_id(self, uid: str) -> User:
        self.__check_users_not_none()
        for u in self.__users:
            if u.id == uuid.UUID(hex=uid):
                assets = AssetRepo().get_for_user(u)
                return User(uuid=u.id, username=u.username, stocks=assets)

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

    def __check_users_not_none(self):
        if self.__users is None:
            self.__users = self.__persistence.get_all()
