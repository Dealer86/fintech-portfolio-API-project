from fastapi import APIRouter, Depends

from domain.asset.factory import AssetFactory
from domain.asset.repo import AssetRepo
from domain.user.repo import UserRepo
from domain.user.factory import UserFactory
from api.models import UserAdd, UserInfo, AssetInfoUser, AssetAdd
from persistence.user_file import UserPersistenceFile
from persistence.users_sqlite import UserPersistenceSqlite

users_router = APIRouter(prefix="/users")


def get_user_repo() -> UserRepo:
    # user_persistence = UserPersistenceFile("main_users.json")
    user_persistence = UserPersistenceSqlite()
    return UserRepo(user_persistence)


@users_router.get("", response_model=list[UserInfo])
def get_all_users(repo=Depends(get_user_repo)):
    return repo.get_all()


@users_router.get("/{user_id}", response_model=UserInfo)
def get_user(user_id: str, repo=Depends(get_user_repo)):
    return repo.get_by_id(user_id)


@users_router.post("", response_model=UserInfo)
def create_a_user(new_user: UserAdd, repo=Depends(get_user_repo)):
    user = UserFactory().make_new(new_user.username)
    repo.add(user)
    return user


@users_router.post("/{user_id}/assets", response_model=AssetInfoUser)
def add_asset_to_user(user_id: str, asset: AssetAdd, repo=Depends(get_user_repo)):
    new_asset = AssetFactory().make_new(asset.ticker)
    # TODO homework, if asset exception throw 400/404
    user = repo.get_by_id(user_id)
    # TODO homework, check we have a user otherwise throw exception code 404
    AssetRepo().add_to_user(user, new_asset)
    return new_asset
