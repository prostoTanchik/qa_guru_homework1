from http import HTTPStatus
import requests


def test_service_availability(app_url):
    response = requests.get(app_url)
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.NOT_FOUND), "Сервис недоступен"
