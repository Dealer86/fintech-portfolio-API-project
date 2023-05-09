import json

from domain.asset.asset import Asset
from domain.asset.persistence_interface import AssetPersistenceInterface
from domain.exceptions import DuplicateAsset
from domain.user.user import User


class AssetPersistenceFile(AssetPersistenceInterface):
    def __init__(self, filename: str):
        self.__filename = filename

    def add_to_user(self, user: User, asset: Asset):
        data = self.__load_json()
        user_assets = data.get(str(user.id), [])
        for every_dict in user_assets:
            print(every_dict)
            if every_dict["ticker"] == asset.ticker:
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

    def delete_for_user(self, user: str, asset: str):
        data = self.__load_json()
        if user in data:
            for d in data[user]:
                if d["ticker"] == asset:
                    data[user].remove(d)
                    break
        with open(self.__filename, "w") as f:
            json.dump(data, f, indent=4)

    def get_for_user(self, user: User) -> list[Asset]:
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
        return assets

    def __load_json(self) -> dict[str, list[dict[str, any]]]:
        try:
            with open(self.__filename) as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
