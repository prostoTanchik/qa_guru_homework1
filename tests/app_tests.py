from http import HTTPStatus
from faker import Faker
from app.models.User import User
import math
import pytest
import requests


@pytest.fixture
def create_users(app_url):
    fake = Faker()
    created_ids = []

    def _create(count: int = 1):
        users = []
        for _ in range(count):
            user = {
                "email": fake.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "avatar": fake.url(),
            }
            response = requests.post(f"{app_url}/api/users", json=user)
            response.raise_for_status()
            data = response.json()
            created_ids.append(data["id"])
            users.append(data)
        return users
    yield _create
    for user_id in created_ids:
        try:
            requests.delete(f"{app_url}/api/users/{user_id}")
        except Exception:
            pass
    #обработка исключения задана на случай, если в последующем микросервис
    #будет выбрасывать исключение при прогоне теста с удалением юзера, т.к.
    #юзер уже был удален в самом тесте


@pytest.fixture
def generate_test_data(app_url):
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


@pytest.fixture
def list_of_users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK
    user_list = response.json()
    for user in user_list:
        User.model_validate(user)
    return response.json()


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.fixture
def default_users_per_page():
    return 3


@pytest.fixture
def users_ids_counter(list_of_users):
    return len([user["id"] for user in list_of_users["items"]])


def calculate_expected_values(total_items, page_size, page_num):
    total_pages = math.ceil(total_items/page_size)
    is_last_page = page_num == total_pages

    if total_items == 0:
        expected_items = 0
    elif is_last_page:
        expected_items = total_items % page_size or page_size
    else:
        expected_items = page_size

    return {
        "page": page_num,
        "size": page_size,
        "pages": total_pages,
        "items": expected_items
    }


def test_get_users(app_url, create_users):
    users = create_users(8)
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK
    user_list = response.json()
    for user in user_list:
        User.model_validate(user)


def test_users_no_duplicates(app_url, create_users):
    users = create_users(8)
    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


def test_get_user(app_url, create_users):
    users = create_users(1)
    user_id = users[0]["id"]
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    user = response.json()
    User.model_validate(user)


def test_create_user(app_url, generate_test_data):
    user_data = generate_test_data
    response = requests.post(f"{app_url}/api/users", json=user_data)
    user_id = response.json()["id"]
    assert response.status_code == HTTPStatus.CREATED
    requests.delete(f"{app_url}/api/users/{user_id}")


def test_patch_user(app_url, create_users):
    user = {
            "email": "john.doe@test.com",
            "first_name": "John",
            "last_name": "Doe",
            "avatar": "https://reqres.in/img/faces/1-image.jpg"}
    users = create_users(1)
    user_id = users[0]["id"]
    response = requests.patch(f"{app_url}/api/users/{user_id}", json=user)
    assert response.status_code == HTTPStatus.OK


def test_delete_user(app_url, create_users):
    users = create_users(1)
    user_id = users[0]["id"]
    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    response_get = requests.get(f"{app_url}/api/users/{user_id}")
    assert response_get.status_code == HTTPStatus.NOT_FOUND


def test_user_flow(app_url, create_users, generate_test_data):
    users = create_users(1)
    user_id = users[0]["id"]
    response_get = requests.get(f"{app_url}/api/users/{user_id}")
    assert response_get.status_code == HTTPStatus.OK
    user = response_get.json()
    User.model_validate(user)
    user_data = generate_test_data
    response_patch = requests.patch(f"{app_url}/api/users/{user_id}", json=generate_test_data)
    assert response_patch.status_code == HTTPStatus.OK
    user = response_patch.json()
    User.model_validate(user)


def test_patch_not_allowed_on_users_collection(app_url):
    response = requests.patch(f"{app_url}/api/users")
    assert response.status_code == 405


def test_patch_unprocessable_entity(app_url, create_users):
    invalid_data = {
        "email": "not-an-email"
    }
    users = create_users(1)
    user_id = users[0]["id"]
    response = requests.patch(f"{app_url}/api/users/{user_id}", json=invalid_data)
    assert response.status_code == 422


