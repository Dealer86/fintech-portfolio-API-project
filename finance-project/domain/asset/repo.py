import logging
import sqlite3
from domain.asset.asset import Asset
from domain.asset.persistence_interface import AssetPersistenceInterface
from domain.exceptions import DuplicateAsset
from domain.user.user import User


class AssetRepo:
    def __init__(self, persistence: AssetPersistenceInterface):
        self.__persistence = persistence
        self.__assets = {}

    def add_to_user(self, user: User, asset: Asset):
        logging.info(
            f"AssetRepo executing add to user command for user with id {str(user.id)}..."
        )
        if asset.ticker in [a.ticker for a in self.get_for_user(user)]:
            logging.warning(
                f"Asset with ticker {asset.ticker} already added for user {user.username}"
            )
            raise DuplicateAsset(
                f"Asset with ticker {asset.ticker} already added for user {user.username}, try another ticker!"
            )
        self.__persistence.add_to_user(user, asset)
        logging.info(
            f"AssetRepo succesfully executed add to user command for user with id {str(user.id)}"
        )
        # Clear user's cache when adding new asset data
        if str(user.id) in self.__assets:
            del self.__assets[str(user.id)]

    def get_for_user(self, user: User) -> list[Asset]:
        logging.info("AssetRepo executing get for user command...")
        # Check if user's crypto data is cached
        if str(user.id) in self.__assets:
            logging.info("AssetRepo succesfully executed get for user command...")
            return self.__assets[str(user.id)]

        # If not cached, fetch from the database and cache it
        asset_list = self.__persistence.get_for_user(user)
        self.__assets[str(user.id)] = asset_list
        logging.info("AssetRepo succesfully executed get for user command...")
        return asset_list

    def delete_for_user(self, user_id: str, asset: str):
        logging.info(
            f"AssetRepo executing delete for user with id {user_id} command..."
        )
        self.__persistence.delete_for_user(user_id, asset)
        logging.info(
            f"AssetRepo succesfully executed delete for user with id {user_id} command..."
        )
        # Clear user's cache when deleting crypto data
        if user_id in self.__assets:
            del self.__assets[user_id]

    def update_unit_number_of_assets_for_user(
        self, user: User, asset: str, units_number: float
    ):
        logging.info(
            f"AssetRepo executing update_unit_number_of_assets_for_user for user with id {str(user.id)} command..."
        )
        self.__persistence.update_unit_number_of_assets_for_user(
            user, asset, units_number
        )
        logging.info(
            f"AssetRepo successfully executed update_unit_number_of_assets_for_user for user with id {str(user.id)} command..."
        )
        # Clear user's cache when updating crypto units
        if str(user.id) in self.__assets:
            del self.__assets[str(user.id)]
