import sqlite3
import logging

from domain.asset.asset import Asset
from domain.asset.persistence_interface import AssetPersistenceInterface
from domain.exceptions import DuplicateAsset, InvalidUserTable
from domain.user.user import User


class AssetPersistenceSqlite(AssetPersistenceInterface):
    def add_to_user(self, user: User, asset: Asset):
        table = f"{user.id}-assets".replace("-", "_")
        with sqlite3.connect(f"main_users.db") as conn:
            cursor = conn.cursor()
            logging.info(f"Executing add_to_user command for user {user.username}...")
            try:
                cursor.execute(
                    f"INSERT INTO '{table}' (ticker, name, country, units, sector)"
                    f"VALUES ('{asset.ticker}', '{asset.name}', "
                    f"'{asset.country}', {asset.units}, '{asset.sector}')"
                )
                logging.info(
                    f"Successfully added asset {asset.ticker} to user {user.username}"
                )
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    logging.warning(f"Asset <{asset.ticker}> already in database!")
                    raise DuplicateAsset(
                        f"Asset <{asset.ticker}> already in database! "
                    )
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    logging.warning(
                        f"Failed executing command add_to_user to add asset to user {user.username} list."
                        f"Reason: " + str(e)
                    )
                    logging.info("Creating table...")
                    cursor.execute(
                        f"CREATE TABLE '{table}'"
                        f" (ticker TEXT PRIMARY KEY,"
                        f" name TEXT,"
                        f" country TEXT,"
                        f" units REAL,"
                        f" sector TEXT)"
                    )
                    logging.info(f"Inserting into {table}")
                    cursor.execute(
                        f"INSERT INTO '{table}' (ticker, name, country, units, sector)"
                        f"VALUES ('{asset.ticker}', '{asset.name}', "
                        f"'{asset.country}', {asset.units}, '{asset.sector}')"
                    )
                conn.commit()

    def get_for_user(self, user: User) -> list[Asset]:
        table = f"{user.id}-assets".replace("-", "_")
        with sqlite3.connect(f"main_users.db") as conn:
            cursor = conn.cursor()
            logging.info(f"Executing get_for_user command for user {user.username}...")
            try:
                cursor.execute(f"SELECT * FROM '{table}'")
                logging.info(
                    f"Successfully executed get_for_user command for user {user.username}"
                )
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    logging.warning(
                        f"Failed executing command get_for_user for getting"
                        f" assets lists for user {user.username}."
                        f"Reason: " + str(e)
                    )
                    return []
                else:
                    raise e
            assets_info = cursor.fetchall()
        assets = [
            Asset(ticker=x[0], nr=x[3], name=x[1], country=x[2], sector=x[4])
            for x in assets_info
        ]
        return assets

    def delete_for_user(self, user_id: str, asset: str):
        table = f"{user_id}-assets".replace("-", "_")
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            logging.info(
                f"Executing delete_for_user command for deleting asset {asset} from user"
                f" with id {user_id} ..."
            )
            try:
                cursor.execute(f"DELETE FROM '{table}' WHERE ticker = ?", (asset,))
                logging.info(
                    f"Successfully executed delete_for_user command for deleting {asset} from"
                    f" user with id {user_id}"
                )
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    logging.warning(
                        f"Could not executed delete_for_user command for deleting"
                        f" asset {asset} for user with id {user_id}. "
                        f"Reason: " + str(e)
                    )
                    raise InvalidUserTable(
                        f"Could not delete asset {asset} for user with id {user_id}, "
                        f"reason: " + str(e)
                    )
                else:
                    raise e
