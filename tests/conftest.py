import os
import dotenv
import pytest
from config import Server
from api.api_client import UsersApi, StatusApi


def pytest_addoption(parser):
    parser.addoption("--env", default="dev")


@pytest.fixture
def users_api(request):
    env = request.config.getoption("--env", default="dev")
    server = Server(env)
    return UsersApi(server.base_url)

@pytest.fixture
def status_api(request):
    env = request.config.getoption("--env", default="dev")
    server = Server(env)
    return StatusApi(server.base_url)