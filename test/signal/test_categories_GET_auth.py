from flask import url_for
from app.__common import HttpStatus
from test.utils.assertions import assert_json_response, assert_header_value
import json


class TestGetActionForSignalCategoriesEndpoint:
    def test_getting_categories_should_return_code_200(self, app, create_authorization_headers, test_client):
        with app.app_context(), app.test_request_context():
            url = url_for('signal_api.categorylistresource', _external=False)

            # test with get action
            get_response = test_client.get(url, headers=create_authorization_headers)
            assert get_response.status_code == HttpStatus.HTTP_200_OK

    def test_getting_categories_should_return_in_json(self, app, create_authorization_headers, test_client):
        with app.app_context(), app.test_request_context():
            url = url_for('signal_api.categorylistresource', _external=False)

            # test with get action
            get_response = test_client.get(url, headers=create_authorization_headers)
            assert_header_value('Content-Type', 'application/json', get_response.headers)


class TestWhenNoCategoryExists:
    def test_getting_categories_should_return_a_blank_list(self, app, create_authorization_headers,
                                                           test_client):
        with app.app_context(), app.test_request_context():
            url = url_for('signal_api.categorylistresource', _external=False)

            # test with get action
            get_response = test_client.get(url, headers=create_authorization_headers)
            assert_json_response([], get_response)


class TestWhenACategoryExists:
    def test_getting_categories_should_return_a_list_with_one_category(self, app, create_auth_user,
                                                                       create_authorization_headers,
                                                                       create_single_category,
                                                                       test_client):
        with app.app_context(), app.test_request_context():
            url = url_for('signal_api.categorylistresource', _external=False)

            # test with get action
            get_response = test_client.get(url, headers=create_authorization_headers)
            assert get_response.status_code == HttpStatus.HTTP_200_OK
            returned_list = json.loads(get_response.data.decode('utf-8'))
            assert len(returned_list) == 1


class TestWhenManyCategoriesExists:
    def test_getting_categories_should_return_a_list_with_many_categories(self, app, create_auth_user,
                                                                        create_authorization_headers,
                                                                        create_categories,
                                                                        test_client):
        with app.app_context(), app.test_request_context():
            url = url_for('signal_api.categorylistresource', _external=False)

            # test with get action
            get_response = test_client.get(url, headers=create_authorization_headers)
            assert get_response.status_code == HttpStatus.HTTP_200_OK
            returned_list = json.loads(get_response.data.decode('utf-8'))
            assert len(returned_list) > 1
