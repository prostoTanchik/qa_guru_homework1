import requests

class UsersApi:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def get_users(self):
        return self.session.get(
            f"{self.base_url}/api/users"
        )

    def get_user(self, user_id: int):
        return self.session.get(
            f"{self.base_url}/api/users/{user_id}"
        )

    def create_user(self, payload: dict):
        return self.session.post(
            f"{self.base_url}/api/users",
            json=payload
        )

    def update_user(self, user_id: int, payload: dict):
        return self.session.patch(
            f"{self.base_url}/api/users/{user_id}",
            json=payload
        )

    def delete_user(self, user_id: int):
        return self.session.delete(
            f"{self.base_url}/api/users/{user_id}"
        )

class StatusApi:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()


    def get_status(self):
        return self.session.get(
            f"{self.base_url}/status"
        )
