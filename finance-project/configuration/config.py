import json

from persistence.user_file import UserPersistenceFile
from persistence.users_sqlite import UserPersistenceSqlite


class InvalidPersistence(Exception):
    pass


def set_persistence_type(file_path):
    with open(file_path, "r") as f:
        json_config_info = f.read()
        user_config_choice = json.loads(json_config_info)

        if user_config_choice.get("persistence") == "sqlite":
            return UserPersistenceSqlite()
        elif user_config_choice.get("persistence") == "file":
            return UserPersistenceFile("main_users.json")
        else:
            raise InvalidPersistence(
                "Unknown persistence type, choose between sqlite or file in config.json"
            )
