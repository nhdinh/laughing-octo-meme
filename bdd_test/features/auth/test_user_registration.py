from pytest_bdd import scenario, given, when, then, parsers
import json


@scenario('test_user_registration.feature', 'New Registration')
def test_new_user_registration():
    pass


@scenario('test_user_registration.feature', 'Duplicated registration')
def test_duplicated_registration():
    pass


@scenario('test_user_registration.feature', 'Registration with simple password')
def test_simple_password_registration():
    pass


@scenario('test_user_registration.feature', 'Registration with no data provided')
def test_no_data_registration():
    pass


@given(parsers.parse("I have username {username} with password {password}"))
def given_having_name_and_password(world, username, password):
    world['post_user'] = {
        'name': username,
        'password': password
    }


@when(parsers.parse("I request the resource '{resource}' with {method} method"))
def when_request_resource(world, __bdd_request_resource, resource, method):
    payload = world.get('post_user', {})
    response = __bdd_request_resource(endpoint=resource, method=method, auth=False, payload=payload)
    world['response'] = response


@then(parsers.parse("I should see return {expected_code} code"))
def assert_response_code(world, expected_code):
    expected_code = int(expected_code)
    response = world['response']
    assert response.status_code == expected_code


@then(parsers.parse("I should see return message '{expected_message}'"))
def assert_response_message(world, expected_message):
    response = world['response']
    data = json.loads(response.data.decode('utf-8'))

    assert data['message'] == expected_message
