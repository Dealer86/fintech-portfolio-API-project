import logging

from fastapi import APIRouter, Depends, HTTPException

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
    logging.info("Fetching all users...")
    users = repo.get_all()
    logging.info("Successfully fetched all users")
    return users


@users_router.get("/{user_id}", response_model=UserInfo)
def get_user(user_id: str, repo=Depends(get_user_repo)):
    logging.info(f"Fetching user with ID {user_id}...")
    user = repo.get_by_id(user_id)
    logging.info(f"Successfully fetched user with ID {user_id}")
    return user


@users_router.delete("/{user_id}")
def delete_user(user_id: str, repo=Depends(get_user_repo)):
    logging.info(f"Deleting user with id {user_id}")
    repo.delete(user_id)
    logging.info(f"Successfully deleted user with id {user_id}")
    return {"status": f"Successfully deleted user with id {user_id}"}


@users_router.delete("/{user_id}/assets")
def delete_asset_for_user(user_id: str, asset: str, asset_repo=Depends(get_asset_repo)):
    logging.info(f"Deleting asset {asset} for user with id {user_id}")
    asset_repo.delete_for_user(user_id, asset)
    logging.info(f"Successfully deleted asset {asset} for user with id {user_id}")


@users_router.patch("/{user_id}/username", response_model=UserInfo)
def update_user(user_id: str, username: str, repo=Depends(get_user_repo)):
    logging.info(f"Updating user with id {user_id} and new username {username}...")
    UserFactory.validate_username(username)
    repo.update(user_id, username)
    logging.info(f"Successfully update user {username} with ID {user_id}")
    return repo.get_by_id(user_id)


@users_router.patch("/{users_id}/units_number", response_model=UserInfo)
def update_unit_number_of_assets_for_user(
    users_id: str,
    asset: str,
    units_number: float,
    asset_repo=Depends(get_asset_repo),
    repo=Depends(get_user_repo),
):
    logging.info(f"Updating asset '{asset}' unit number for user with ID {users_id}...")
    our_user = repo.get_by_id(users_id)
    asset_repo.update_unit_number_of_assets_for_user(our_user, asset, units_number)
    logging.info(
        f" Successfully updated asset '{asset}' unit number for user with ID {users_id}."
    )
    return repo.get_by_id(users_id)


@users_router.post("", response_model=UserInfo)
def create_a_user(new_user: UserAdd, repo=Depends(get_user_repo)):
    logging.info(f"Creating user with username: '{new_user.username}'...")
    user = UserFactory().make_new(new_user.username)
    repo.add(user)
    logging.info(f"Successfully created user {user.username}")
    return user


@users_router.post("/{user_id}/assets", response_model=AssetInfoUser)
def add_asset_to_user(
    user_id: str,
    asset: AssetAdd,
    repo=Depends(get_user_repo),
    asset_repo=Depends(get_asset_repo),
):
    logging.info("Creating a new asset...")
    new_asset = AssetFactory().make_new(asset.ticker)
    logging.info(f"Successfully created asset {asset.ticker}")

    logging.info(f"Getting user with id {user_id}...")
    user = repo.get_by_id(user_id)
    logging.info(f"User {user.username} with id {user_id} found")

    logging.info(f"Adding asset {asset.ticker} to user {user.username}...")
    asset_repo.add_to_user(user, new_asset)
    logging.info(
        f"Successfully added asset {asset.ticker} to user with username {user.username}"
    )

    return new_asset
