import json


def setup_test_env():
    raise NotImplemented


def teardown_test_env():
    raise NotImplemented


def get_json_from_response(response):
    response_string = response.data.decode('utf-8')

    return json.loads(response_string)


def get_header_value(header_key, response_headers):
    try:
        return next(h[1] for h in response_headers.items() if h[0] == header_key)
    except StopIteration:
        return None
