import json
from base64 import b64encode


def get_json_from_response(response):
    response_string = response.data.decode('utf-8')

    return json.loads(response_string)


def get_header_value(header_key, response_headers):
    try:
        return next(h[1] for h in response_headers.items() if h[0] == header_key)
    except StopIteration:
        return None


def get_accept_content_type_headers():
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def get_authentication_headers(username, password):
    authentication_headers = get_accept_content_type_headers()
    authentication_headers['Authorization'] = 'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode(
        'utf-8')

    return authentication_headers
