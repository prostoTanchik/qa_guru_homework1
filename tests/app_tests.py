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


def test_get_users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK
    users = response.json()
    for user in users:
        User.model_validate(user)


def test_users_no_dublicate(list_of_users, users_ids_counter):
    assert len(users_ids_counter) == len(set(users_ids_counter))


@pytest.mark.parametrize("user_id", [i for i in range(1, 12)])
def test_get_user(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    user = response.json()
    User.model_validate(user)


@pytest.mark.parametrize("page_size", [i for i in range(1, 13)])
def test_size_of_page(app_url, list_of_users, page_size, users_ids_counter):
    max_page = math.ceil(users_ids_counter / page_size)

    for page_num in range(1, max_page + 1):
        response = requests.get(f"{app_url}/api/users?page={page_num}&size={page_size}")
        assert response.status_code == HTTPStatus.OK
        expected = calculate_expected_values(users_ids_counter, page_size, page_num)
        response_data = response.json()
        print(response_data)
        assert response_data["page"] == expected["page"]
        assert response_data["size"] == expected["size"]
        assert response_data["pages"] == expected["pages"]
        assert len(response_data["items"]) == expected["items"]


@pytest.mark.parametrize("page_size", [i for i in range(1, 13)])
def test_page_quantity(app_url, list_of_users, page_size, users_ids_counter):
    max_page = math.ceil(users_ids_counter / page_size)
    for page_num in range(1, max_page + 1):
        expected = calculate_expected_values(users_ids_counter, page_size, page_num)
        response = requests.get(f"{app_url}/api/users?page={page_num}&size={page_size}")
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()
        assert len(response_data["items"]) == expected["items"]
        assert response_data["pages"] == max_page


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


