import abc

from domain.user.user import User


class UserPersistenceInterface(abc.ABC):
    @abc.abstractmethod
    def add(self, user: User):
        pass

    @abc.abstractmethod
    def get_all(self) -> list[User]:
        pass

    @abc.abstractmethod
    def delete(self, uid: str):
        pass

    @abc.abstractmethod
    def update(self, user_id: str, new_username: str):
        pass
