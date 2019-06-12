from flask import url_for
from app.__common import HttpStatus
from test.utils.helpers import create_authentication_headers
from test.utils.assertions import assert_json_response, assert_header_value
from flask import g
import pytest, json


class TestWhenUnauthorized:
    def test_all_actions_should_return_code_401(self, app, test_client):
        with app.app_context(), app.test_request_context():
            url = url_for('signal_api.categorylistresource', _external=False)

            # test with get action
            get_response = test_client.get(url)
            assert get_response.status_code == HttpStatus.HTTP_401_UNAUTHORIZED

            # test with post action
            post_response = test_client.post(url, data={})
            assert post_response.status_code == HttpStatus.HTTP_401_UNAUTHORIZED

            url_with_id = url_for('signal_api.categoryresource', identifier=1, _external=False)

            # test with delete action
            delete_response = test_client.delete(url_with_id)
            assert delete_response.status_code == HttpStatus.HTTP_401_UNAUTHORIZED

            # test with patch action
            patch_response = test_client.patch(url_with_id)
            assert patch_response.status_code == HttpStatus.HTTP_401_UNAUTHORIZED
