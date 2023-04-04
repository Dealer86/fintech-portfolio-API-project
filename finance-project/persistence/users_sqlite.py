import sqlite3
from domain.user.persistance_interface import UserPersistenceInterface
from domain.user.user import User


class UserPersistenceSqlite(UserPersistenceInterface):
    def get_all(self) -> list[User]:
        return []

    def add(self, user: User):
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"INSERT INTO users (id, username) VALUES ('{user.id}', '{user.username}')")
            except sqlite3.OperationalError as e:
                if "no such table: users" in str(e):
                    cursor.execute("CREATE TABLE users (id TEXT PRIMARY KEY, username TEXT NOT NULL)")
                else:
                    raise e
                cursor.execute(f"INSERT INTO users (id, username) VALUES ('{user.id}', '{user.username}')")
            conn.commit()
