import json

import pytest
from flask import g, url_for

from app.__common import DbInstance
from app.app_factory import create_app
from test.utils.helpers import get_accept_content_type_headers
from base64 import b64decode, b64encode


@pytest.fixture
def app(request):
    app = create_app('testing')
    app.debug = True
    app.testing = True

    db = DbInstance.get()

    # setup testing env
    with app.app_context():
        db.init_app(app)
        db.create_all()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield app

    # teardown testing env
    def teardown():
        db.session.close()
        db.drop_all()
        ctx.pop()

    request.addfinalizer(teardown)

    return app


@pytest.fixture
def test_client(app):
    test_client = app.test_client()
    return test_client


@pytest.fixture
def create_user(app, test_client):
    with app.app_context(), app.test_request_context():
        if 'test_user' not in g:
            g.test_user_username = 'the_user'
            g.test_user_password = 'P@ssw0rd!'

        data = {'name': g.test_user_username, 'password': g.test_user_password}

        url = url_for('auth_api.userlistresource', _external=False)
        response = test_client.post(url, headers=get_accept_content_type_headers(), data=json.dumps(data))

        return response


@pytest.fixture
def create_authorization_header(app, test_client):
    with app.app_context(), app.test_request_context():
        if 'test_user' not in g:
            g.test_user_username = 'the_user'
            g.test_user_password = 'P@ssw0rd!'

        authentication_headers = get_accept_content_type_headers()
        authentication_headers['Authorization'] = 'Basic ' + b64encode(
            (g.test_user_username + ':' + g.test_user_password).encode('utf-8')).decode(
            'utf-8')

        return authentication_headers
