# bdd_test/conftest.py

from app.__common import DbInstance, HttpStatus
from app.app_factory import create_app
from bdd_test.helpers import __bdd_create_logger, __bdd_create_request_headers

from base64 import b64encode
import pytest
from flask import g, url_for
import json

logger = __bdd_create_logger()


@pytest.fixture(scope='class')
def world():
    return {}


@pytest.fixture(scope='class')
def app(request):
    app = create_app('testing')
    app.debug = True
    app.testing = True
    logger.info('Setup *App* & begin testing session')

    db = DbInstance.get()
    # setup testing env
    with app.app_context():
        logger.info('Init db and create all schemas')
        db.init_app(app)
        db.create_all()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield app

    # teardown testing env
    def teardown():
        logger.info('Drop database & App teardown')
        db.session.close()
        db.drop_all()
        ctx.pop()

    request.addfinalizer(teardown)

    return app


@pytest.fixture(scope='class')
def test_client(app, request):
    logger.info('Setup *Test_client*')
    test_client = app.test_client()

    yield test_client

    def teardown():
        logger.info('*Test_client teardown*')

    request.addfinalizer(teardown)
    return test_client


@pytest.fixture(scope='class')
def __bdd_create_auth_user(app, test_client, request):
    with app.app_context(), app.test_request_context():
        logger.info('Setup *Create_user&')

        if 'test_user' not in g:
            g.test_user_username = 'the_user'
            g.test_user_password = 'P@ssw0rd!'

        data = {'name': g.test_user_username, 'password': g.test_user_password}

        url = url_for('auth_api.userlistresource', _external=False)
        response = test_client.post(url, headers=__bdd_create_request_headers(), data=json.dumps(data))

    def teardown():
        # No need to teardown as all the schema and data will be drop in app_teardown
        logger.info('*Create_user* teardown')

    request.addfinalizer(teardown)

    return response


@pytest.fixture(scope='class')
def __bdd_create_auth_headers(app, test_client, __bdd_create_auth_user):
    create_auth_response = __bdd_create_auth_user

    if create_auth_response is not None and create_auth_response.status_code == HttpStatus.HTTP_201_CREATED:
        with app.app_context(), app.test_request_context():
            logger.info('Stating create auth headers and return')

            if 'test_user' not in g:
                g.test_user_username = 'the_user'
                g.test_user_password = 'P@ssw0rd!'

            auth_headers = __bdd_create_request_headers()
            auth_headers['Authorization'] = 'Basic ' + b64encode(
                (g.test_user_username + ':' + g.test_user_password).encode('utf-8')).decode(
                'utf-8')

            return auth_headers
    else:
        logger.debug('Create_auth_user failed so that cannot construct authorization header')
        return None


@pytest.fixture(scope='class')
def __bdd_request_resource(app, test_client):
    def __request_resource(endpoint=None, method='GET', auth=False, payload=None):
        # return None if resource is not specified
        if endpoint is None or endpoint == '':
            return None

        # create the request headers
        with app.app_context(), app.test_request_context():
            headers = __bdd_create_request_headers() if auth is False else __bdd_create_auth_headers()

            # do method and return the response
            endpoint = str(endpoint)

            if str(method).lower() == 'get':
                response = test_client.get(endpoint, headers=headers)
            elif str(method).lower() == 'post':
                response = test_client.post(endpoint, headers=headers, data=json.dumps(payload))
            else:
                # TODO: Need to finalize with PUT, PATCH and DELETE
                response = None

            return response

    return __request_resource
