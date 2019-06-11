from flask import g

from app.__common.http_status import HttpStatus
from test.utils.assertions import assert_header_value, assert_json_response
from test.utils.helpers import get_authentication_headers


class TestApplicationWhenNoAuthorization:
    def test_app_should_return_code_401(self, test_client):
        response = test_client.get('/')
        assert response.status_code == HttpStatus.HTTP_401_UNAUTHORIZED


class TestApplicationWhenAuthorized:
    def test_app_should_return_code_200(self, create_user, create_authorization_header, test_client):
        response = test_client.get('/', headers=create_authorization_header)
        assert response.status_code == HttpStatus.HTTP_200_OK

    def test_app_should_return_data_in_json(self, create_user, create_authorization_header, test_client):
        response = test_client.get('/', headers=create_authorization_header)
        assert_header_value('Content-Type', 'application/json', response.headers)

    def test_app_should_return_hello_world(self, create_user, create_authorization_header, test_client):
        response = test_client.get('/', headers=create_authorization_header)
        assert_json_response({'hello': 'world'}, response)
