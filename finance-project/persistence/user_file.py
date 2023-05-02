import json
import logging
import uuid

from domain.asset.repo import AssetRepo
from domain.user.factory import UserFactory
from domain.user.persistence_interface import UserPersistenceInterface
from domain.user.user import User


class FailToWriteToFile(Exception):
    pass


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
            logging.warning(
                "Could not read file because it not exists, will return empty list, reason: "
                + str(e)
            )
            return []

    def add(self, user: User):
        current_users = self.get_all()
        current_users.append(user)
        users_info = [(str(x.id), x.username, x.stocks) for x in current_users]
        users_json = json.dumps(users_info)
        try:
            with open(self.__file_path, "w") as f:
                f.write(users_json)
        except FailToWriteToFile as e:
            logging.error("Could not write file. Error: " + str(e))

    def delete(self, uid: str):
        current_users = self.get_all()
        updated_users_list = [u for u in current_users if u.id != uuid.UUID(hex=uid)]
        users_info = [(str(x.id), x.username, x.stocks) for x in updated_users_list]
        json_current_users = json.dumps(users_info)
        try:
            with open(self.__file_path, "w") as f:
                f.write(json_current_users)
        except FailToWriteToFile as e:
            logging.error("Could not delete from file. Error: " + str(e))

    def update(self, user_id: str, new_username: str):
        current_users = self.get_all()
        for user in current_users:
            if user.id == uuid.UUID(hex=user_id):
                user.username = new_username
                break
        users_info = [(str(u.id), u.username, u.stocks) for u in current_users]
        users_json = json.dumps(users_info)
        try:
            with open(self.__file_path, "w") as f:
                f.write(users_json)
        except FailToWriteToFile as e:
            logging.error("Could not update file. Error: " + str(e))
