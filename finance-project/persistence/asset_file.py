import json
import logging

from domain.asset.factory import AssetFactory
from domain.user.factory import UserFactory
from domain.asset.asset import Asset
from domain.asset.persistence_interface import AssetPersistenceInterface
from domain.exceptions import DuplicateAsset
from domain.user.user import User
from persistence.user_file import UserPersistenceFile


class AssetPersistenceFile(AssetPersistenceInterface):
    def __init__(self, filename: str):
        self.__filename = filename

    def add_to_user(self, user: User, asset: Asset):
        user_repo = UserPersistenceFile("main_users.json")
        user_list = user_repo.get_all()
        for u in user_list:
            if str(u.id) == str(user.id):
                u.stocks.append(asset)

        self.save_to_file(user_list)

    def delete_for_user(self, user_id: str, asset: Asset):
        pass

    def get_for_user(self, user: User) -> list[Asset]:
        return user.stocks

    def save_to_file(self, user_list: list[User]):
        data = [u.to_tuple() for u in user_list]
        data_prep = json.dumps(data, indent=4)

        with open(self.__filename, "w") as f:
            f.write(data_prep)
