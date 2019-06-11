# __init__.py

import flask


def signal_blueprint_registry() -> flask.Blueprint:
    from flask_restful import Api
    from app.signal_blueprint.category_resources import CategoryResource, CategoryListResource
    from app.signal_blueprint.message_resources import MessageResource, MessageListResource

    api_bp = flask.Blueprint('signal_api', __name__)
    api = Api(api_bp)

    api.add_resource(CategoryListResource, '/categories')
    api.add_resource(CategoryResource, '/categories/<int:identifier>')
    api.add_resource(MessageListResource, '/messages')
    api.add_resource(MessageResource, '/messages/<int:identifier>')

    return api_bp
