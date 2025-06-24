import os
import dotenv
import pytest


@pytest.fixture(autouse=True)
def env():
    dotenv.load_dotenv()


@pytest.fixture
def app_url():
    return os.getenv("APP_URL")
