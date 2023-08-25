from domain.asset.asset import Asset
from domain.asset.asset_observer import AssetObserver
import logging

from domain.user.user import User


class AssetLoggingObserver(AssetObserver):
    def asset_added(self, user_id: str, asset: Asset):
        logging.info(f"Asset added for user {user_id}: {asset.name}")

    def asset_updated(self, user: User, asset: str, units_number: float):
        logging.info(
            f"Asset updated for user {user.id}: {asset} with units number {units_number}"
        )

    def asset_deleted(self, user_id: str, asset: str):
        logging.info(f"Asset deleted for user {user_id}: {asset}")

    def asset_already_added(self, user_id: str, asset: str):
        logging.warning(f"Asset already added for user {user_id}: {asset}")
