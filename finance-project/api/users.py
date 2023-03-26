from fastapi import APIRouter

from domain.user.repo import UserRepo
from domain.user.factory import UserFactory
from api.models import UserAdd, UserInfo

users_router = APIRouter(prefix="/users")

repo = UserRepo("main_users.json")


@users_router.get("", response_model=list[UserInfo])
def get_all_users():
    return repo.get_all()


@users_router.get("{/username}", response_model=UserInfo)
def get_user(username: str):
    return repo.get_by_username(username)


@users_router.post("")
def create_a_user(new_user: UserAdd):
    user = UserFactory().make(new_user.username)
    repo.add(user)


@users_router.delete("")
def delete_a_user(name: str):
    repo.delete(name)
