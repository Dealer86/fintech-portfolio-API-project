import json

from domain.asset.asset import Asset
from domain.asset.factory import AssetFactory
from domain.asset.persistence_interface import AssetPersistenceInterface
from domain.user.user import User


class AssetPersistenceFile(AssetPersistenceInterface):
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def add_to_user(self, user: User, asset: Asset):
        pass

    def get_for_user(self, user: User) -> list[Asset]:
        pass
