import uuid

from domain.asset.factory import AssetFactory
from domain.exceptions import InvalidUsername
from domain.user.user import User


class UserFactory:
    @classmethod
    def make_new(cls, username: str) -> User:
        if len(username) < 6:
            raise InvalidUsername("Username should have at least 6 characters")
        if len(username) > 20:
            raise InvalidUsername("Username should have a maximum of 20 characters")
        username_split = username.split("-")
        username_str = ""
        for u in username_split:
            username_str += u
        if not username_str.isalnum():
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

    @classmethod
    def from_tuple(cls, info: tuple) -> User:
        asset_obj = [AssetFactory.from_tuple(a) for a in info[2]]
        return User(uuid=uuid.UUID(info[0]), username=info[1], stocks=asset_obj)
