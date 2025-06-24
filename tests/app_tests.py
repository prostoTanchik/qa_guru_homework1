from http import HTTPStatus
from models.User import User
import math
import pytest
import requests


@pytest.fixture
def list_of_users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.fixture
def default_users_per_page():
    return 3


def total_pages(list_of_users, users_per_page):
    total_users = len(list_of_users["items"])
    return math.ceil(total_users/users_per_page)


def test_get_users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK
    users = response.json()
    for user in users:
        User.model_validate(user)


def test_users_no_dublicate(list_of_users):
    users_ids = [user["id"] for user in list_of_users["items"]]
    assert len(users_ids) == len(set(users_ids))


@pytest.mark.parametrize("user_id", [i for i in range(1, 12)])
def test_get_user(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    user = response.json()
    User.model_validate(user)


@pytest.mark.parametrize("page_num", [1, 2, 3, 4])
def test_size_of_page(app_url, list_of_users, page_num, default_users_per_page):
    response = requests.get(f"{app_url}/api/users?page={page_num}&size={default_users_per_page}")
    assert response.status_code == HTTPStatus.OK
    pages_quantity = total_pages(list_of_users, default_users_per_page)
    users = response.json()
    users_ids = len([user["id"] for user in list_of_users["items"]])
    if page_num < pages_quantity:
        assert len(users["items"]) == default_users_per_page
    elif page_num == pages_quantity:
        assert len(users["items"]) in [users_ids % default_users_per_page, default_users_per_page]


@pytest.mark.parametrize("page_size", [1, 3, 12, 13])
def test_page_quantity(app_url, list_of_users, page_size):
    pages_quantity = total_pages(list_of_users, page_size)
    response = requests.get(f"{app_url}/api/users?page={pages_quantity}&size={page_size}")
    assert response.status_code == HTTPStatus.OK
    users = response.json()
    assert users["items"] != 0


def test_no_dublicate_pages(app_url, list_of_users, default_users_per_page):
    pages = [1, 2, 3, 4]
    all_user_ids = set()
    for page in pages:
        response = requests.get(f"{app_url}/api/users?page={page}&size={default_users_per_page}")
        assert response.status_code == HTTPStatus.OK
        users = response.json()
        current_page_ids = {user["id"] for user in users["items"]}
        assert all_user_ids.isdisjoint(current_page_ids)
        all_user_ids.update(current_page_ids)


