import logging
from domain.asset.asset import Asset
from domain.asset.persistence_interface import AssetPersistenceInterface
from domain.exceptions import DuplicateAsset
from domain.user.user import User
from domain.asset.asset_observer import AssetObserver
from domain.asset.logging_observer import AssetLoggingObserver

logger = AssetLoggingObserver()


class AssetRepo:
    def __init__(self, persistence: AssetPersistenceInterface):
        self.__persistence = persistence
        self.__assets = {}
        self.__observers = []

    def add_observer(self, observer: AssetObserver):
        self.__observers.append(observer)

    def remove_observer(self, observer: AssetObserver):
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify_observers_asset_added(self, user_id: str, asset: Asset):
        for observer in self.__observers:
            observer.asset_added(user_id, asset)

    def notify_observers_asset_updated(
        self, user: User, asset: str, unit_number: float
    ):
        for observer in self.__observers:
            observer.asset_updated(user, asset, unit_number)

    def notify_observers_asset_deleted(self, user_id: str, asset: Asset):
        for observer in self.__observers:
            observer.asset_deleted(user_id, asset)

    def notify_observers_asset_already_added(self, user_id: str, asset: Asset):
        for observer in self.__observers:
            observer.asset_already_added(user_id, asset)

    def add_to_user(self, user: User, asset: Asset):
        if asset.ticker in [a.ticker for a in self.get_for_user(user)]:
            self.add_observer(logger)
            self.notify_observers_asset_already_added(str(user.id), asset)
            raise DuplicateAsset(
                f"Asset with ticker {asset.ticker} already added for user {user.username}, try another ticker!"
            )

        self.__persistence.add_to_user(user, asset)
        self.add_observer(logger)
        self.notify_observers_asset_added(str(user.id), asset)
        # Clear user's cache when adding new asset data
        if str(user.id) in self.__assets:
            del self.__assets[str(user.id)]

    def get_for_user(self, user: User) -> list[Asset]:
        # Check if user's crypto data is cached
        if str(user.id) in self.__assets:
            return self.__assets[str(user.id)]
        logging.info("AssetRepo executing get for user command...")
        # If not cached, fetch from the database and cache it
        asset_list = self.__persistence.get_for_user(user)
        self.__assets[str(user.id)] = asset_list
        return asset_list

    def delete_for_user(self, user_id: str, asset: str):
        self.__persistence.delete_for_user(user_id, asset)
        self.add_observer(logger)
        self.notify_observers_asset_deleted(user_id, asset)
        # Clear user's cache when deleting crypto data
        if user_id in self.__assets:
            del self.__assets[user_id]

    def update_unit_number_of_assets_for_user(
        self, user: User, asset: str, units_number: float
    ):
        self.__persistence.update_unit_number_of_assets_for_user(
            user, asset, units_number
        )
        self.add_observer(logger)
        self.notify_observers_asset_updated(user, asset, units_number)
        # Clear user's cache when updating crypto units
        if str(user.id) in self.__assets:
            del self.__assets[str(user.id)]
