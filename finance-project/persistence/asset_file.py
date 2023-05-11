import json
import logging

from domain.asset.asset import Asset
from domain.asset.persistence_interface import AssetPersistenceInterface
from domain.exceptions import DuplicateAsset
from domain.user.user import User


class AssetPersistenceFile(AssetPersistenceInterface):
    def __init__(self, filename: str):
        self.__filename = filename

    def add_to_user(self, user: User, asset: Asset):
        logging.info("AssetPersistenceFile executing delete for user command ...")
        data = self.__load_json()
        user_assets = data.get(str(user.id), [])
        for every_dict in user_assets:
            print(every_dict)
            if every_dict["ticker"] == asset.ticker:
                logging.warning(
                    "AssetPersistenceFile add to user command failed because of duplicate asset"
                )
                raise DuplicateAsset(f"Asset {asset.ticker} already added")
        user_assets.append(
            {
                "ticker": asset.ticker,
                "name": asset.name,
                "country": asset.country,
                "nr": asset.units,
                "sector": asset.sector,
            }
        )
        data[str(user.id)] = user_assets
        with open(self.__filename, "w") as f:
            json.dump(data, f, indent=4)
            logging.info(
                "AssetPersistenceFile add to user command successfully executed"
            )

    def delete_for_user(self, user: str, asset: str):
        logging.info("AssetPersistenceFile executing delete for user command ...")
        data = self.__load_json()
        if user in data:
            for d in data[user]:
                if d["ticker"] == asset:
                    data[user].remove(d)
                    break
        with open(self.__filename, "w") as f:
            json.dump(data, f, indent=4)
            logging.info(
                "AssetPersistenceFile delete for user was successfully executed"
            )

    def get_for_user(self, user: User) -> list[Asset]:
        logging.info("AssetPersistenceFile executing get for user command ...")
        data = self.__load_json()
        user_assets = data.get(str(user.id), [])
        assets = []
        for asset_dict in user_assets:
            asset = Asset(
                ticker=asset_dict["ticker"],
                name=asset_dict["name"],
                country=asset_dict["country"],
                nr=asset_dict["nr"],
                sector=asset_dict["sector"],
            )
            assets.append(asset)
        logging.info(
            "AssetPersistenceFile get for user command was successfully executed"
        )
        return assets

    def __load_json(self) -> dict[str, list[dict[str, any]]]:
        try:
            with open(self.__filename) as f:
                return json.load(f)
        except FileNotFoundError as e:
            logging.warning(
                "Could not read file because it not exists, will return empty dict, reason: "
                + str(e)
            )
            return {}
