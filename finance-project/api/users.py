from fastapi import APIRouter

users_router = APIRouter(prefix="/users")


@users_router.get("/")
def get_all_users():
    return []


@users_router.post("/")
def create_a_user():
    pass
