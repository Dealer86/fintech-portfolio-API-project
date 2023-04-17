import abc

from domain.asset.asset import Asset
from domain.user.user import User


class UserPersistenceInterface(abc.ABC):
    @abc.abstractmethod
    def add(self, user: User):
        pass

    @abc.abstractmethod
    def get_all(self) -> list[User]:
        pass

    @abc.abstractmethod
    def get_by_id(self, uid: str) -> User:
        pass

    @abc.abstractmethod
    def delete_by_id(self, uid: str):
        pass

