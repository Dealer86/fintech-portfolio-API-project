import json

from configuration.config import InvalidPersistence
from persistence.asset_sqlite import AssetPersistenceSqlite


def set_asset_persistence_type(file_path: str):
    with open(file_path, "r") as f:
        content = f.read()
    user_config_choice = json.loads(content)
    if user_config_choice.get("persistence") == "sqlite":
        return AssetPersistenceSqlite()
    elif user_config_choice.get("persistence") == "file":
        pass
    else:
        raise InvalidPersistence(
            "Unknown persistence type, choose between sqlite or file in config.json"
        )
