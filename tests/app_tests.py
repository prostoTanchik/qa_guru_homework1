from http import HTTPStatus
from faker import Faker
from app.models.User import User
import math
import pytest
import requests


@pytest.fixture
def create_users(users_api):
    fake = Faker()
    created_ids = []

    def _create(count: int = 1):
        users = []

        for _ in range(count):
            payload = {
                "email": fake.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "avatar": fake.url(),
            }

            response = users_api.create_user(payload)
            response.raise_for_status()

            data = response.json()
            created_ids.append(data["id"])
            users.append(data)

        return users

    yield _create

    for user_id in created_ids:
        try:
            users_api.delete_user(user_id)
        except Exception:
            pass


@pytest.fixture
def generate_test_data():
    fake = Faker()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    avatar_url = fake.url()
    user = {"email": email,
            "first_name": first_name,
            "last_name": last_name,
            "avatar": avatar_url}
    yield user


def test_get_users(create_users, users_api):
    users = create_users(8)
    response = users_api.get_users()
    assert response.status_code == HTTPStatus.OK
    user_list = response.json()
    for user in user_list:
        User.model_validate(user)


def test_users_no_duplicates(create_users):
    users = create_users(8)
    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


def test_get_user(create_users, users_api):
    users = create_users(1)
    user_id = users[0]["id"]
    response = users_api.get_user(int(user_id))
    assert response.status_code == HTTPStatus.OK
    user = response.json()
    User.model_validate(user)


def test_create_user(generate_test_data, users_api):
    user_data = generate_test_data
    response = users_api.create_user(user_data)
    user_id = response.json()["id"]
    assert response.status_code == HTTPStatus.CREATED
    users_api.delete_user(int(user_id))


def test_patch_user(create_users, users_api):
    user = {
            "email": "john.doe@test.com",
            "first_name": "John",
            "last_name": "Doe",
            "avatar": "https://reqres.in/img/faces/1-image.jpg"}
    users = create_users(1)
    user_id = users[0]["id"]
    response = users_api.update_user(int(user_id), payload=user)
    assert response.status_code == HTTPStatus.OK


def test_delete_user(create_users, users_api):
    users = create_users(1)
    user_id = users[0]["id"]
    response = users_api.delete_user(int(user_id))
    assert response.status_code == HTTPStatus.OK
    response_get = users_api.get_user(int(user_id))
    assert response_get.status_code == HTTPStatus.NOT_FOUND


def test_user_flow(create_users, generate_test_data, users_api):
    users = create_users(1)
    user_id = users[0]["id"]
    response_get = users_api.get_user(int(user_id))
    assert response_get.status_code == HTTPStatus.OK
    user = response_get.json()
    User.model_validate(user)
    user_data = generate_test_data
    response_patch = users_api.update_user(int(user_id), payload=user_data)
    assert response_patch.status_code == HTTPStatus.OK
    user = response_patch.json()
    User.model_validate(user)


def test_patch_unprocessable_entity(create_users, users_api):
    invalid_data = {
        "email": "not-an-email"
    }
    users = create_users(1)
    user_id = users[0]["id"]
    response = users_api.update_user(int(user_id), payload=invalid_data)
    assert response.status_code == 422


