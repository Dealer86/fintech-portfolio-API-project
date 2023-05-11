import logging
import sqlite3
from domain.asset.asset import Asset
from domain.asset.persistence_interface import AssetPersistenceInterface

from domain.user.user import User


class AssetRepo:
    def __init__(self, persistence: AssetPersistenceInterface):
        self.__persistence = persistence
        self.__assets = None

    def add_to_user(self, user: User, asset: Asset):
        logging.info("AssetRepo executing add to user command...")
        self.__persistence.add_to_user(user, asset)
        self.__check_we_have_assets(user)
        self.__assets.append(asset)

    def get_for_user(self, user: User) -> list[Asset]:
        logging.info("AssetRepo executing get for user command...")
        self.__check_we_have_assets(user)
        return self.__assets

    def delete_for_user(self, user_id: str, asset: str):
        logging.info("AssetRepo executing delete for user command...")
        self.__persistence.delete_for_user(user_id, asset)

    def __check_we_have_assets(self, user: User):
        if self.__assets is None:
            self.__assets = self.__persistence.get_for_user(user)
