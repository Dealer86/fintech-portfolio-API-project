from abc import ABC, abstractmethod

from domain.asset.asset import Asset
from domain.user.user import User


class AssetObserver(ABC):
    @abstractmethod
    def asset_deleted(self, user_id: str, asset: Asset):
        pass

    @abstractmethod
    def asset_already_added(self, user_id: str, asset: str):
        pass

    @abstractmethod
    def asset_added(self, user_id: str, asset: Asset):
        pass

    @abstractmethod
    def asset_updated(self, user: User, asset: str, units_number: float):
        pass
