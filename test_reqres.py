import pytest
import requests


@pytest.fixture(scope="module")
def shared_data():
    return {"id": None}


def test_create_user(shared_data):
    url = "https://reqres.in/api/users"
    headers = {'x-api-key': 'reqres-free-v1'}
    body = {"name": "john", "job": "qa"}
    expected_status_code = 201

    response = requests.post(url, headers=headers, json=body)
    response_status = response.status_code
    response_body = response.json()
    shared_data["id"] = response_body["id"]

    assert response_status == expected_status_code


def test_read_user():
    user_id = 12
    # url = f"https://reqres.in/api/users/{user_id}"
    url = f"http://127.0.0.1:8000/api/users/{user_id}"
    headers = {'x-api-key': 'reqres-free-v1'}
    expected_email = "rachel.howell@reqres.in"
    expected_name = "Rachel"

    response = requests.get(url, headers=headers)
    body = response.json()
    # data = body["data"]

    # assert data["email"] == expected_email
    # assert data["first_name"] == expected_name

    assert body["email"] == expected_email
    assert body["first_name"] == expected_name


def test_update_user(shared_data):
    user_id = shared_data["id"]
    url = f"https://reqres.in/api/users/{user_id}"
    headers = {'x-api-key': 'reqres-free-v1'}
    new_data = {"name": "hannah",
                "job": "qa"}
    expected_status_code = 200

    response = requests.put(url, headers=headers, data=new_data)
    response_status_code = response.status_code

    assert response_status_code == expected_status_code


def test_delete_user(shared_data):
    user_id = 13
    url = f"https://reqres.in/api/users/{user_id}"
    headers = {'x-api-key': 'reqres-free-v1'}
    expected_status_code = 204
    response = requests.delete(url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == expected_status_code
