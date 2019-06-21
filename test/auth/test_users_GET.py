from app.__common.http_status import HttpStatus


class TestWhenNoUserExists:
    def test_getting_resource_shall_return_unauthorized(self, test_client):
        response = test_client.get('/')
        assert response.status_code == HttpStatus.HTTP_401_UNAUTHORIZED


class TestWhenUserExists:
    def test_getting_resource_shall_return_code_200(self, __bdd_create_auth_user, test_client,
                                                    __bdd_create_auth_headers):
        response = test_client.get('/', headers=__bdd_create_auth_headers)
        assert response.status_code == HttpStatus.HTTP_200_OK
