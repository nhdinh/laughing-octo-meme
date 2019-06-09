# app/app.py

import os
from flask import Flask
from flask_restful import Api, Resource
from app.__common import AuthRequiredResource
import logging, logging.config
from config import basedir
import yaml


def __create_logger(default_path='/logging.conf.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
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


def create_app(config_name: str) -> Flask:
    """
    Create and return Flask app
    :param config_name: specified config_env for the app, default: Development
    :return: Flask app
    """
    app = Flask(__name__)
    app.logger = __create_logger()

    try:
        # trying to create the app from requested environment
        app.config.from_object('config.{config_name}Config'.format(
            config_name=config_name.lower().capitalize()))
    except Exception as ex:
        app.logger.debug(str(ex))
        app.logger.info(
            'Load config config_name="{config_name}" failed. Load DevelopmentConfig instead'.format(
                config_name=config_name))

        # failed-safe, use the default Development environment
        app.config.from_object('config.DevelopmentConfig')

    # init db
    from app.__common import DbInstance
    DbInstance.get().init_app(app)

    # turn off checking trailing slash in route
    app.url_map.strict_slashes = False

    # set api_prefix
    app.config['URL_PREFIX'] = '/api/v1'

    # create a helloworld resource
    api = Api(app)
    api.add_resource(HelloWorld, '/')
    from app.__common.auth_blueprint import auth_blueprint_registry
    app.register_blueprint(auth_blueprint_registry(), url_prefix=app.config['URL_PREFIX'])

    return app


class HelloWorld(AuthRequiredResource):
    def get(self):
        return {'hello': 'world'}
