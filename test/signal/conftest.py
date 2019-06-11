import pytest
from flask import url_for, jsonify


@pytest.fixture
def create_category(app, create_user, create_authorization_header, test_client):
    def _create_category(category_name: str):
        with app.app_context(), app.test_request_context():
            url = url_for('signal_api.categorylistresource', _external=False)
            payload = {"name": category_name}

            return test_client.post(url, data=jsonify(payload), headers=create_authorization_header)

    return _create_category
