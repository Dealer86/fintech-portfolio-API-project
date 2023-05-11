import uuid
import logging

from domain.exceptions import InvalidUsername
from domain.user.user import User


class UserFactory:
    @classmethod
    def make_new(cls, username: str) -> User:
        logging.info(
            f"Executing make_new command to create new user with username {username} ..."
        )
        if len(username) < 6:
            logging.error(
                "Command make_new failed because username length was below 6 chars"
            )
            raise InvalidUsername("Username should have at least 6 characters")
        if len(username) > 20:
            logging.error(
                "Command make_new failed because username length was above 6 chars"
            )
            raise InvalidUsername("Username should have a maximum of 20 characters")
        for char in username:
            if not (char.isalnum() or char == "-"):
                logging.error(
                    "Command make_new failed because username should contain only"
                    " alpha-numeric characters or '-'"
                )
                raise InvalidUsername(
                    "Username should contain only alpha-numeric characters or '-'"
                )
        user_uuid = uuid.uuid4()
        logging.info(f"Successfully executed make_new command for user {username}")
        return User(user_uuid, username)

    @classmethod
    def make_from_persistence(cls, info: tuple) -> User:
        return User(
            uuid=uuid.UUID(info[0]),
            username=info[1],
        )
