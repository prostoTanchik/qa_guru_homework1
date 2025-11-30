from http import HTTPStatus
from typing import Iterable

from fastapi import APIRouter, HTTPException
from fastapi_pagination import paginate, Page

from app.database import users
from app.models.User import User, UserCreate, UserUpdate

router = APIRouter(prefix="/api/users")


@router.get("/")
async def get_users() -> Iterable[User]:
    return users.get_users()


@router.get("/{user_id}")
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(user: User) -> User:
    UserCreate.model_validate(user.model_dump())
    return users.create_user(user)


@router.patch("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, user: UserUpdate) -> User:
    if user_id < 1:
        raise HTTPException(status_code=422, detail="Invalid user id")
    user_data = user.model_dump(exclude_unset=True)
    return users.update_user(user_id, user_data)

@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    users.delete_user(user_id)
    return {"message": "User deleted successfully"}


