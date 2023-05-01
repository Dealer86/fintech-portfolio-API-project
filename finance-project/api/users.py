import logging

from fastapi import APIRouter, Depends

from configuration.asset_config import set_asset_persistence_type
from configuration.config import set_persistence_type
from domain.asset.factory import AssetFactory
from domain.asset.repo import AssetRepo
from domain.user.repo import UserRepo
from domain.user.factory import UserFactory
from api.models import UserAdd, UserInfo, AssetInfoUser, AssetAdd


users_router = APIRouter(prefix="/users")


def get_asset_repo() -> AssetRepo:
    asset_persistence = set_asset_persistence_type("configuration/config.json")
    return AssetRepo(asset_persistence)


def get_user_repo() -> UserRepo:
    user_persistence = set_persistence_type("configuration/config.json")
    return UserRepo(user_persistence)


@users_router.get("", response_model=list[UserInfo])
def get_all_users(repo=Depends(get_user_repo)):
    return repo.get_all()


@users_router.get("/{user_id}", response_model=UserInfo)
def get_user(user_id: str, repo=Depends(get_user_repo)):
    return repo.get_by_id(user_id)


@users_router.delete("/{user_id}")
def delete_user(user_id: str, repo=Depends(get_user_repo)):
    repo.delete(user_id)
    return {"status": "ok"}


@users_router.put("/{user_id}", response_model=UserInfo)
def update_user(user_id: str, username: str, repo=Depends(get_user_repo)):
    repo.update(user_id, username)
    return repo.get_by_id(user_id)


@users_router.post("", response_model=UserInfo)
def create_a_user(new_user: UserAdd, repo=Depends(get_user_repo)):
    logging.info("Creating a user...")
    user = UserFactory().make_new(new_user.username)
    try:
        repo.add(user)
        logging.info(f"Successfully created user {user.username}")
    except Exception as e:
        logging.error("Error could not create a user. Reason: " + str(e))
    return user


@users_router.post("/{user_id}/assets", response_model=AssetInfoUser)
def add_asset_to_user(
    user_id: str,
    asset: AssetAdd,
    repo=Depends(get_user_repo),
    asset_repo=Depends(get_asset_repo),
):
    new_asset = AssetFactory().make_new(asset.ticker)
    user = repo.get_by_id(user_id)
    asset_repo.add_to_user(user, new_asset)
    return new_asset
