import json
from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Query
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.customization import CustomizedPage, UseParamsFields
from typing import TypeVar
from models.AppStatus import AppStatus
from models.User import User

app = FastAPI()
add_pagination(app)


users: list[User] = []


@app.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users))


@app.get("/api/users")
async def get_users() -> Page[User]:
    return paginate(users)


@app.get("/api/users/{user_id}")
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users[user_id - 1]


if __name__ == "__main__":
    import uvicorn
    with open("users.json") as f:
        users = json.load(f)
    for user in users:
        User.model_validate(user)
    uvicorn.run(app, host="127.0.0.1", port=8000)