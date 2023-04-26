import uuid

from domain.exceptions import InvalidUsername
from domain.user.user import User


class UserFactory:
    @classmethod
    def make_new(cls, username: str) -> User:
        if len(username) < 6:
            raise InvalidUsername("Username should have at least 6 characters")
        if len(username) > 20:
            raise InvalidUsername("Username should have a maximum of 20 characters")
        for char in username:
            if not (char.isalnum() or char == "-"):
                raise InvalidUsername(
                    "Username should contain only alpha-numeric characters or '-'"
                )
        user_uuid = uuid.uuid4()
        return User(user_uuid, username)

    @classmethod
    def make_from_persistence(cls, info: tuple) -> User:
        return User(
            uuid=uuid.UUID(info[0]),
            username=info[1],
        )
