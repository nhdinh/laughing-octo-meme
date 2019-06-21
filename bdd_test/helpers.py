from config import basedir
import os
import logging, logging.config
import yaml, json
from app.__common import HttpStatus


def __bdd_create_logger(default_path='/logging.conf.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    Setup logging configuration and create logger
    """
    path = basedir + default_path
    value = os.getenv(env_key, None)

    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

    logger = logging.getLogger(__name__)

    return logger


def __bdd_get_json_from_response(response):
    """
    Load json from response
    :param response: the response object as a input
    :return: json string
    """
    response_string = response.data.decode('utf-8')

    return json.loads(response_string)


def get_header_value(header_key, response_headers):
    """
    Get value by the header's key
    :param header_key:
    :param response_headers:
    :return:
    """
    try:
        return next(h[1] for h in response_headers.items() if h[0] == header_key)
    except StopIteration:
        return None


def __bdd_create_request_headers():
    """
    Create accept content-type header
    :return:
    """
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def __bdd_get_id_from_created_response(response):
    """
    Get id from a 'created' response
    :param response: a 'created' response
    :return: a created object's id
    """
    if response.status_code == HttpStatus.HTTP_201_CREATED:
        response_json_string = response.data.decode('utf-8')
        created_object = json.loads(response_json_string)

        return int(created_object['id'])

    return None
