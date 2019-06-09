# app/app.py

from flask import Flask
from flask_restful import Api, Resource


def create_app() -> Flask:
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(HelloWorld, '/')

    return app


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
