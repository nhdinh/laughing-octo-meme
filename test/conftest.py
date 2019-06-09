import pytest

from app.app import create_app


@pytest.fixture
def test_client():
    app = create_app('testing')
    app.debug = True

    return app.test_client()


@pytest.fixture
def create_auth(test_client):
    user = 'nhdinh'
    password = 'nhd!nhP@ssW0rd'

    return test_client.post('/api/v1/users', {'name': user, 'password': password})


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(test_client):
    return AuthActions(test_client)
