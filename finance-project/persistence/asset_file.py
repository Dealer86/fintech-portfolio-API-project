import json
import logging
import os

from domain.exceptions import NonExistentUserId
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

    def update_unit_number_of_assets_for_user(
        self, user: User, asset: str, units_number: float
    ):
        user_list = self.get_all()
        for u in user_list:
            if str(u.id) == str(user.id):
                stock = [u for u in u.stocks if u.ticker == asset]
                for s in stock:
                    s.units = units_number
        self.__save_to_file(user_list)

    def delete_for_user(self, user_id: str, asset: str):
        logging.info(
            f"Asset Persistence File executing delete_for_user command for user with id{user_id} and asset {asset}"
        )
        user_list = self.get_all()
        for user in user_list:
            if str(user.id) == user_id:
                user.stocks = [a for a in user.stocks if a.ticker != asset]
                logging.info(
                    f"Asset Persistence File successfully executed delete_for_user command for user with "
                    f"id{user_id} and asset {asset}"
                )
                break
        else:
            raise NonExistentUserId(f"User with id {user_id} does not exist")
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
