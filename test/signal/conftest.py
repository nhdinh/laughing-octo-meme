import pytest, json
from flask import url_for
from test.utils.helpers import create_logger, get_id_from_created_response

logger = create_logger()


@pytest.fixture(scope='function')
def create_single_category(app, __bdd_create_auth_headers, test_client, request):
    """
    Create single category
    :param app: fixture
    :param create_authorization_headers: fixture
    :param test_client: fixture
    :param request: fixture
    :return: void
    """
    category = 'category_name'
    logger.info('Create category name="{name}"'.format(name=category))
    with app.app_context(), app.test_request_context():
        url = url_for('signal_api.categorylistresource', _external=False)
        created_response = test_client.post(url, data=json.dumps({"name": category}),
                                            headers=__bdd_create_auth_headers)

        created_category_id = get_id_from_created_response(created_response)

    yield create_single_category

    def teardown():
        with app.app_context(), app.test_request_context():
            logger.info('Delete category')
            url = url_for('signal_api.categoryresource', identifier=created_category_id, _external=False)
            test_client.delete(url, headers=__bdd_create_auth_headers)

    request.addfinalizer(teardown)
    return


@pytest.fixture(scope='function')
def create_categories(app, __bdd_create_auth_headers, test_client, request):
    """
    Create 3 categories fixture
    :param app: fixture
    :param create_authorization_headers: fixture
    :param test_client: fixture
    :param request: fixture
    :return: void
    """
    categories = ['category 1', 'category 2', 'category 3']
    category_indice = []

    with app.app_context(), app.test_request_context():
        for category in categories:
            logger.info('Create category name="{name}"'.format(name=category))
            url = url_for('signal_api.categorylistresource', _external=False)
            created_response = test_client.post(url, data=json.dumps({"name": category}),
                                                headers=__bdd_create_auth_headers)

            created_category_id = get_id_from_created_response(created_response)

        category_indice.append(created_category_id)

    yield create_categories

    def teardown():
        with app.app_context(), app.test_request_context():
            logger.info('Delete categories')
            for cat_id in category_indice:
                url = url_for('signal_api.categoryresource', identifier=cat_id, _external=False)
                test_client.delete(url, headers=__bdd_create_auth_headers)

    request.addfinalizer(teardown)
    return
