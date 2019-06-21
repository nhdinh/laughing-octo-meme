from flask import g, request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from app.__common import DbInstance
from app.__common import PaginationHelper, HttpStatus
from .auth import AuthRequiredResource, auth
from .user_models import User, UserSchema

from app.app_factory import __create_logger

logger = __create_logger()


@auth.verify_password
def verify_user_password(name, password):
    user = User.query.filter_by(name=name).first()
    if not user or not user.verify_password(password):
        return False

    g.user = user
    return True


class UserResource(AuthRequiredResource):
    __user_schema = UserSchema()

    def get(self, identifier):
        user = User.query.get_or_404(identifier)
        result = self.__user_schema.dump(user).data
        return result


class UserListResource(Resource):
    __user_schema = UserSchema()

    @auth.login_required
    def get(self):
        pagination_helper = PaginationHelper(
            request,
            query=User.query,
            resource_for_url='auth_api.userlistresource',
            key_name='users',
            schema=self.__user_schema)
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {'message': 'No input data provided'}
            return response, HttpStatus.HTTP_400_BAD_REQUEST

        errors = self.__user_schema.validate(request_dict)
        if errors:
            return errors, HttpStatus.HTTP_400_BAD_REQUEST

        name = request_dict['name']
        existing_user = User.query.filter_by(name=name).first()
        if existing_user is not None:
            logger.debug('An user with the same name "{username}" already exists'.format(username=name))
            response = {'message': 'An user with the same name already exists'}
            return response, HttpStatus.HTTP_400_BAD_REQUEST

        try:
            user = User(name=name)
            error_message, password_ok = user.check_password_strength_and_hash_if_ok(request_dict['password'])

            if password_ok:
                user.add(user)
                query = User.query.get(user.id)
                result = self.__user_schema.dump(query).data
                result['auth_token'] = user.generate_token().decode()
                return result, HttpStatus.HTTP_201_CREATED
            else:
                return {"error": error_message}, HttpStatus.HTTP_400_BAD_REQUEST
        except SQLAlchemyError as e:
            DbInstance.get().session.rollback()
            resp = {"error": str(e)}
            return resp, HttpStatus.HTTP_400_BAD_REQUEST
