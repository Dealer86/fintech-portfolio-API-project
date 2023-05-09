from abc import ABC, abstractmethod

from domain.asset.asset import Asset
from domain.user.user import User


class AssetPersistenceInterface(ABC):
    @abstractmethod
    def add_to_user(self, user: User, asset: Asset):
        pass

    @abstractmethod
    def get_for_user(self, user: User) -> list[Asset]:
        pass

    @abstractmethod
    def delete_for_user(self, user_id: str, asset: str):
        pass
