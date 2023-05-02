import logging
import sqlite3

from domain.user.persistence_interface import UserPersistenceInterface
from domain.user.user import User
from domain.user.factory import UserFactory


class UserPersistenceSqlite(UserPersistenceInterface):
    def get_all(self) -> list[User]:
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM users")
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    logging.warning(f"No users found into database, error: {str(e)}")
                    return []
                else:
                    raise e
            users_info = cursor.fetchall()
            factory = UserFactory()
        users = [factory.make_from_persistence(x) for x in users_info]
        return users

    def add(self, user: User):
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    f"INSERT INTO users (id, username) VALUES ('{user.id}', '{user.username}')"
                )
                logging.info(
                    f"Successfully added user with id {user.id} and {user.username} into database"
                )
            except sqlite3.OperationalError as e:
                if "no such table: users" in str(e):
                    cursor.execute(
                        "CREATE TABLE users (id TEXT PRIMARY KEY, username TEXT NOT NULL)"
                    )
                else:
                    logging.error(
                        f"Could not create new table into database: " + str(e)
                    )
                    raise e
                cursor.execute(
                    f"INSERT INTO users (id, username) VALUES ('{user.id}', '{user.username}')"
                )
            conn.commit()

    def delete(self, uid: str):
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"DELETE FROM users WHERE id = '{uid}'")
            except sqlite3.OperationalError as e:
                logging.error(f"Could not delete from database, error:  " + str(e))
                raise e
            conn.commit()

    def update(self, user_id: str, new_username: str):
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    f"UPDATE users SET (username)='{new_username}' WHERE id='{user_id}'"
                )
            except sqlite3.OperationalError as e:
                logging.error("Could not update database, reason: " + str(e))
                raise e
            conn.commit()
