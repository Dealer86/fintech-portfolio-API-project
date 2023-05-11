import logging
import uuid

from domain.asset.persistence_interface import AssetPersistenceInterface
from domain.exceptions import NonExistentUserId, DuplicateUser
from domain.user.persistence_interface import UserPersistenceInterface

from singleton import singleton
from domain.asset.repo import AssetRepo
from configuration.asset_config import set_asset_persistence_type

from domain.user.user import User


@singleton
class UserRepo:
    def __init__(
        self, persistence: UserPersistenceInterface, asset: AssetPersistenceInterface
    ):
        print("Initializing user repo")
        self.__persistence = persistence
        self.__users = None
        self.__asset = asset

    def add(self, new_user: User):
        logging.info("UserRepo executing add command...")
        self.__check_we_have_users()
        if new_user.username in [u.username for u in self.__users]:
            logging.error("UserRepo add command failed because of duplicate user")
            raise DuplicateUser(
                f"User {new_user.username} already exists, try another username"
            )

        self.__persistence.add(new_user)

        self.__users.append(new_user)
        logging.info("UserRepo add command was successfully executed")

    def get_all(self) -> list[User]:
        logging.info("UserRepo executing get all command...")
        self.__check_we_have_users()
        return self.__users

    def get_by_id(self, uid: str) -> User:
        logging.info("UserRepo executing get by id command...")
        self.__check_we_have_users()
        self.__check_id(uid)

        for u in self.__users:
            if u.id == uuid.UUID(hex=uid):
                assets = self.__asset.get_for_user(u)
                logging.info("UserRepo get by id command was successfully executed")
                return User(
                    uuid=u.id,
                    username=u.username,
                    stocks=assets,
                )

    def delete(self, uid: str):
        logging.info("UserRepo executing delete command...")
        self.__check_we_have_users()
        self.__check_id(uid)
        self.__persistence.delete(uid)
        self.__refresh_cache()
        logging.info("UserRepo delete command was successfully executed")

    def update(self, user_id: str, username: str):
        logging.info("UserRepo executing update command...")
        self.__check_we_have_users()
        self.__check_id(user_id)
        self.__persistence.update(user_id, username)
        self.__refresh_cache()
        logging.info("UserRepo update command was successfully executed")

    def __check_we_have_users(self):
        if self.__users is None:
            self.__users = self.__persistence.get_all()

    def __check_id(self, uid: str):
        if uid not in [str(u.id) for u in self.__users]:
            raise NonExistentUserId(f"User with ID '{uid}' does not exist")

    def __refresh_cache(self):
        self.__users = self.__persistence.get_all()
