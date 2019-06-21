from flask import url_for
from app.__common import HttpStatus
from test.utils.helpers import get_id_from_created_response, create_logger
from test.utils.assertions import assert_json_response, assert_header_value
import json

logger = create_logger()


class TestCreatingCategory:
    def test_creating_category_should_return_code_201(self, app, __bdd_create_auth_headers, test_client, request):
        category = 'category_name'

        with app.app_context(), app.test_request_context():
            url = url_for('signal_api.categorylistresource', _external=False)

            created_response = test_client.post(url, headers=__bdd_create_auth_headers,
                                                data=json.dumps({'name': category}))

            def teardown():
                with app.app_context(), app.test_request_context():
                    created_category_id = get_id_from_created_response(created_response)

                    logger.info('Delete category')
                    url = url_for('signal_api.categoryresource', identifier=created_category_id, _external=False)
                    test_client.delete(url, headers=__bdd_create_auth_headers)

            request.addfinalizer(teardown)

            assert created_response.status_code == HttpStatus.HTTP_201_CREATED

    def test_creating_category_should_return_created_id(self, app, __bdd_create_auth_headers, test_client, request):
        category = 'category_name'

        with app.app_context(), app.test_request_context():
            url = url_for('signal_api.categorylistresource', _external=False)

            created_response = test_client.post(url, headers=__bdd_create_auth_headers,
                                                data=json.dumps({'name': category}))
            id = get_id_from_created_response(created_response)

            get_url = url_for('signal_api.categoryresource', identifier=id, _external=False)
            get_response = test_client.get(get_url, headers=__bdd_create_auth_headers)

            def teardown():
                with app.app_context(), app.test_request_context():
                    created_category_id = get_id_from_created_response(created_response)

                    logger.info('Delete category')
                    url = url_for('signal_api.categoryresource', identifier=created_category_id, _external=False)
                    test_client.delete(url, headers=__bdd_create_auth_headers)

            request.addfinalizer(teardown)

            assert get_response.status_code == HttpStatus.HTTP_200_OK
