class Server:
    def __init__(self, env):
        self.envs = {
            "dev": "http://127.0.0.1:8002",
            "stage": "http://127.0.0.1:8002",
        }

        self.base_url = self.envs[env]