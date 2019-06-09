from flask import Blueprint


def auth_blueprint_registry() -> Blueprint:
    from flask_restful import Api
    from .auth_resource import UserResource, UserListResource

    auth_blueprint = Blueprint('auth_api', __name__)
    api = Api(auth_blueprint)

    api.add_resource(UserResource, '/users/<int:identifier>')
    api.add_resource(UserListResource, '/users')
    return auth_blueprint
