import json
import logging
import os


from domain.user.factory import UserFactory
from domain.asset.asset import Asset
from domain.asset.persistence_interface import AssetPersistenceInterface

from domain.user.user import User


class AssetPersistenceFile(AssetPersistenceInterface):
    def __init__(self, filename: str):
        self.__filename = filename

    def get_all(self) -> list[User]:
        if not os.path.exists(self.__filename):
            return []
        with open(self.__filename) as f:
            content = f.read()
        data = json.loads(content)
        return [UserFactory.from_tuple(u) for u in data]

    def add_to_user(self, user: User, asset: Asset):
        user_list = self.get_all()
        for u in user_list:
            if str(u.id) == str(user.id):
                u.stocks.append(asset)
        self.__save_to_file(user_list)

    def delete_for_user(self, user_id: str, asset: str):
        user_list = self.get_all()
        for user in user_list:
            if str(user.id) == user_id:
                user.stocks = [a for a in user.stocks if a.ticker != asset]
                break
        self.__save_to_file(user_list)

    def get_for_user(self, user: User) -> list[Asset]:
        user_data = self.get_all()
        for u in user_data:
            if str(u.id) == str(user.id):
                return u.stocks

    def __save_to_file(self, user_list: list[User]):
        data = [u.to_tuple() for u in user_list]
        data_prep = json.dumps(data, indent=4)

        with open(self.__filename, "w") as f:
            f.write(data_prep)
