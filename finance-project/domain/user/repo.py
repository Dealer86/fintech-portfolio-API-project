import uuid
import json
from singleton import singleton
from domain.asset.repo import AssetRepo
from domain.user.factory import UserFactory
from domain.user.persistance_interface import UserPersistenceInterface
from domain.user.user import User


@singleton
class UserRepo:
    def __init__(self, persistence: UserPersistenceInterface):
        print("Initializing user repo")
        self.__persistence = persistence
        self.__users = None

    def add(self, new_user: User):
        self.__check_we_have_users()
        self.__persistence.add(new_user)
        self.__users.append(new_user)

    def get_all(self) -> list[User]:
        self.__check_we_have_users()
        return self.__users

    def get_by_id(self, uid: str) -> User:
        self.__check_we_have_users()
        for user in self.__users:
            if str(user.id) == uid:
                return user
            else:
                return self.__persistence.get_by_id(uid)

    def delete(self, uid: str):
        self.__check_we_have_users()
        self.__persistence.delete(uid)
        for user in self.__users:
            if user.id == uuid.UUID(hex=uid):
                self.__users.remove(user)
                break

    def update(self, user_id: str, username: str):
        self.__check_we_have_users()
        self.__persistence.update(user_id, username)
        for user in self.__users:
            if user.id == uuid.UUID(hex=user_id):
                user.username = username

    def __check_we_have_users(self):
        if self.__users is None:
            self.__users = self.__persistence.get_all()
