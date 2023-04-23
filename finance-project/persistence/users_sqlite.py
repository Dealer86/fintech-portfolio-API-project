import sqlite3
from domain.user.persistance_interface import UserPersistenceInterface
from domain.user.user import User
from domain.user.factory import UserFactory
from persistence.exceptions import NonExistentUserId


class UserPersistenceSqlite(UserPersistenceInterface):
    def get_all(self) -> list[User]:
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM users")
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
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
            except sqlite3.OperationalError as e:
                if "no such table: users" in str(e):
                    cursor.execute(
                        "CREATE TABLE users (id TEXT PRIMARY KEY, username TEXT NOT NULL)"
                    )
                else:
                    raise e
                cursor.execute(
                    f"INSERT INTO users (id, username) VALUES ('{user.id}', '{user.username}')"
                )
            conn.commit()

    def get_by_id(self, uid: str) -> User:
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM users WHERE id='{uid}'")

            user_info = cursor.fetchone()
            if not user_info:
                raise NonExistentUserId(f"No user found with ID '{uid}'")

            factory = UserFactory()
            user = factory.make_from_persistence(user_info)

            return user

    def delete_by_id(self, uid: str):
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT id FROM users WHERE id='{uid}'")
            result = cursor.fetchone()
            if result is None:
                raise NonExistentUserId(f"No user found with ID '{uid}'")
            cursor.execute(f"DELETE FROM users WHERE id = '{uid}'")
            conn.commit()
