from domain.user.user import User


class InvalidUsername(Exception):
    pass


class UserFactory:
    def make(self, username: str) -> User:
        if len(username) < 6:
            raise InvalidUsername("Username should have at least 6 characters")
        if len(username) > 20:
            raise InvalidUsername("Username should have a maximum of 20 characters")
        for char in username:
            if not (char.isalnum() or char == "-"):
                raise InvalidUsername(
                    "Username should contain only alpha-numeric characters or '-'"
                )

        return User(username)
