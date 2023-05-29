import logging

from fastapi import APIRouter, Depends

from configuration.asset_config import set_asset_persistence_type
from configuration.config import set_persistence_type
from domain.asset.factory import AssetFactory
from domain.asset.repo import AssetRepo
from domain.exceptions import (
    DuplicateUser,
    DuplicateAsset,
    NonExistentUserId,
    InvalidTicker,
)
from domain.user.repo import UserRepo
from domain.user.factory import UserFactory
from api.models import (
    UserAdd,
    UserInfo,
    AssetInfoUser,
    AssetAdd,
    AssetInfoBase,
    UnitsAdd,
)
from persistence.asset_file import AssetPersistenceFile

users_router = APIRouter(prefix="/users")


def get_asset_repo() -> AssetRepo:
    asset_persistence = set_asset_persistence_type("configuration/config.json")
    return AssetRepo(asset_persistence)


def get_user_repo() -> UserRepo:
    user_persistence = set_persistence_type("configuration/config.json")
    asset_persistence = set_asset_persistence_type("configuration/config.json")
    return UserRepo(user_persistence, asset_persistence)


@users_router.get("", response_model=list[UserInfo])
def get_all_users(repo=Depends(get_user_repo)):
    return repo.get_all()


@users_router.get("/{user_id}", response_model=UserInfo)
def get_user(user_id: str, repo=Depends(get_user_repo)):
    return repo.get_by_id(user_id)


@users_router.delete("/{user_id}")
def delete_user(user_id: str, repo=Depends(get_user_repo)):
    logging.info(f"Deleting user with id {user_id}")
    repo.delete(user_id)
    return {"status": "ok"}


@users_router.delete("/{user_id}/assets")
def delete_asset_for_user(user_id: str, asset: str, asset_repo=Depends(get_asset_repo)):
    logging.info(f"Deleting asset {asset} for user with id {user_id}")
    asset_repo.delete_for_user(user_id, asset)


@users_router.put("/{user_id}", response_model=UserInfo)
def update_user(user_id: str, username: str, repo=Depends(get_user_repo)):
    logging.info(f"Updating user with id {user_id} with new username {username}...")
    try:
        repo.update(user_id, username)
        logging.info(f"Successfully update user {username} with ID {user_id}")
    except NonExistentUserId as e:
        logging.error(str(e))
        raise e
    return repo.get_by_id(user_id)


@users_router.post("", response_model=UserInfo)
def create_a_user(new_user: UserAdd, repo=Depends(get_user_repo)):
    logging.info("Creating a user...")
    user = UserFactory().make_new(new_user.username)
    try:
        repo.add(user)
        logging.info(f"Successfully created user {user.username}")
    except DuplicateUser as e:
        logging.error(str(e))
        raise e
    except Exception as e:
        logging.error("Error could not create a user. Reason: " + str(e))
    return user


@users_router.post("/{user_id}/assets", response_model=AssetInfoUser)
def add_asset_to_user(
    user_id: str,
    asset: AssetAdd,
    units: UnitsAdd,
    repo=Depends(get_user_repo),
    asset_repo=Depends(get_asset_repo),
):
    logging.info("Creating a new asset...")
    try:
        new_asset = AssetFactory().make_new(asset.ticker, units.units)
        logging.info(f"Successfully created asset {asset.ticker}")
    except TypeError:
        logging.warning(f"Invalid ticker {asset.ticker}")
        raise InvalidTicker(f"Invalid ticker {asset.ticker}")
    logging.info(f"Getting user with id {user_id}...")
    try:
        user = repo.get_by_id(user_id)
        logging.info(f"User {user.username} with id {user_id} found")
    except NonExistentUserId as e:
        logging.error(str(e))
        raise e
    logging.info(f"Adding asset {asset.ticker} to user {user.username}...")
    try:
        asset_repo.add_to_user(user, new_asset)
        logging.info(f"Successfully added asset {asset.ticker} to user {user.username}")
    except DuplicateAsset as e:
        logging.error(str(e))
        raise e
    return new_asset
