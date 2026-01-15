from http import HTTPStatus
import requests


def test_service_availability(status_api):
    response = status_api.get_status()
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.NOT_FOUND), "Сервис недоступен"
