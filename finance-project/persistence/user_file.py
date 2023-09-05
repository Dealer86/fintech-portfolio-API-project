import json
import logging
import uuid
import os

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
        if not os.path.exists(self.__file_path):
            return []
        logging.info("UserPersistenceFile executing get all command...")
        try:
            with open(self.__file_path) as f:
                contents = f.read()
            users_info = json.loads(contents)
            factory = UserFactory()
            logging.info(
                "UserPersistenceFile get all command was successfully executed"
            )
            return [factory.make_from_persistence(x) for x in users_info]

        except FailToWriteToFile as e:
            logging.warning(
                "Could not read file because it not exists, will return empty list, reason: "
                + str(e)
            )
            return []

    def add(self, user: User):
        logging.info("UserPersistenceFile executing add command...")
        current_users = self.get_all()
        current_users.append(user)
        users_info = [(str(x.id), x.username, x.stocks) for x in current_users]
        users_json = json.dumps(users_info, indent=4)
        try:
            with open(self.__file_path, "w") as f:
                f.write(users_json)
                logging.info(
                    f"UserPersistenceFile add command successfully executed, added {user.username} to file"
                )
        except FailToWriteToFile as e:
            logging.error("Could not write file. Error: " + str(e))
            raise e

    def delete(self, uid: str):
        logging.info("UserPersistenceFile executing delete command...")
        current_users = self.get_all()
        updated_users_list = [u for u in current_users if u.id != uuid.UUID(hex=uid)]
        users_info = [(str(x.id), x.username, x.stocks) for x in updated_users_list]
        json_current_users = json.dumps(users_info, indent=4)
        try:
            with open(self.__file_path, "w") as f:
                f.write(json_current_users)
                logging.info("UserPersistenceFile delete command successfully executed")
        except FailToWriteToFile as e:
            logging.error("Could not delete from file. Error: " + str(e))
            raise e

    def update(self, user_id: str, new_username: str):
        logging.info("UserPersistenceFile executing update command...")
        UserFactory.validate_username(new_username)
        current_users = self.get_all()
        for user in current_users:
            if user.id == uuid.UUID(hex=user_id):
                user.username = new_username
                break
        users_info = [(str(u.id), u.username, u.stocks) for u in current_users]
        users_json = json.dumps(users_info, indent=4)
        try:
            with open(self.__file_path, "w") as f:
                f.write(users_json)
                logging.info("UserPersistenceFile update command successfully executed")
        except FailToWriteToFile as e:
            logging.error("Could not update file. Error: " + str(e))
            raise e
