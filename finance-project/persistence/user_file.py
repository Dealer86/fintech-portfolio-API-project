import json
import logging
import uuid

from domain.asset.repo import AssetRepo
from domain.user.factory import UserFactory
from domain.user.persistance_interface import UserPersistenceInterface
from domain.user.user import User
from persistence.exceptions import NonExistentUserId


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

        except Exception as e:
            logging.error("Could not read file, reason: " + str(e))
            return []

    def add(self, user: User):
        current_users = self.get_all()
        current_users.append(user)
        users_info = [(str(x.id), x.username, x.stocks) for x in current_users]
        users_json = json.dumps(users_info)
        with open(self.__file_path, "w") as f:
            f.write(users_json)

    def get_by_id(self, uid: str) -> User:
        current_users = self.get_all()
        correct_id = [u for u in current_users if str(u.id) == uid]
        if not correct_id:
            raise NonExistentUserId(f"No user found with ID '{uid}'")

        for u in current_users:
            if u.id == uuid.UUID(hex=uid):
                assets = AssetRepo().get_for_user(u)

                return User(uuid=u.id, username=u.username, stocks=assets)

    def delete(self, uid: str):
        current_users = self.get_all()
        try:
            updated_users_list = [
                u for u in current_users if u.id != uuid.UUID(hex=uid)
            ]
        except ValueError:
            raise NonExistentUserId(f"No user found with ID '{uid}'")
        users_info = [(str(x.id), x.username, x.stocks) for x in updated_users_list]
        json_current_users = json.dumps(users_info)
        with open(self.__file_path, "w") as f:
            f.write(json_current_users)

    def update(self, user_id: str, new_username: str):
        current_users = self.get_all()
        for user in current_users:
            if user.id == uuid.UUID(hex=user_id):
                user.username = new_username
                break
        users_info = [(str(u.id), u.username, u.stocks) for u in current_users]
        users_json = json.dumps(users_info)
        with open(self.__file_path, "w") as f:
            f.write(users_json)
