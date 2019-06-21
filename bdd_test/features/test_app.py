from pytest_bdd import scenario, given, when, then, parsers
from bdd_test.helpers import __bdd_create_request_headers


@scenario('test_app.feature', 'Test application when unauthorized')
def test_application_when_unauthorized():
    pass


@scenario('test_app.feature', 'Test application when authorized')
def test_application_when_authorized():
    pass


@scenario('test_app.feature', 'Test categories endpoint with GET method when authorized')
def test_categories_get_endpoint_when_authorized():
    pass


@scenario('test_app.feature', 'Test categories endpoint with POST method when authorized')
def test_categories_post_endpoint_when_authorized():
    pass


@given("I am unauthorized user")
def given_unauthorized_user(world):
    headers = __bdd_create_request_headers()
    world['request_headers'] = headers

    return headers


@given(r'I am authorized user')
def given_authorized_user(world, __bdd_create_auth_headers):
    headers = __bdd_create_auth_headers
    world['request_headers'] = headers

    return headers


@when(parsers.parse("I request the resource '{resource_endpoint}' with {method} method"))
def request_the_resource(world, test_client, resource_endpoint, method):
    auth_headers = world['request_headers']

    if method == 'GET':
        response = test_client.get(resource_endpoint, headers=auth_headers)
    elif method == 'POST':
        import json
        response = test_client.post(resource_endpoint, headers=auth_headers, data=json.dumps({'name': 'category'}))
    else:
        response = None

    world['response'] = response


@then(parsers.parse('I should see the {expected_status_code:d} message'))
def should_response_with_code(world, expected_status_code):
    expected_status_code = int(expected_status_code)
    response = world['response']
    assert expected_status_code == response.status_code, "Received status_code=%d" % \
                                                         response.status_code
