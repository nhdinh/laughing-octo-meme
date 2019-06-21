import re

from marshmallow import validate, fields
from passlib.apps import custom_app_context as password_context

from app.__common import DbInstance, MarshmallowInstance, AddUpdateDelete
from datetime import timedelta, datetime
import jwt
from flask import current_app

db = DbInstance.get()


class User(db.Model, AddUpdateDelete):
    """
    Model of User
    """
    __tablename__ = 't_users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # I save the hashed password
    hashed_password = db.Column(db.String(120), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def verify_password(self, password):
        return password_context.verify(password, self.hashed_password)

    def check_password_strength_and_hash_if_ok(self, password):
        if len(password) < 8:
            return 'The password is too short', False

        if len(password) > 32:
            return 'The password is too long', False

        if re.search(r'[A-Z]', password) is None:
            return 'The password must include at least one uppercase letter', False

        if re.search(r'[a-z]', password) is None:
            return 'The password must include at least one lowercase letter', False

        if re.search(r'\d', password) is None:
            return 'The password must include at least one number', False

        if re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None:
            return 'The password must include at least one symbol', False

        self.hashed_password = password_context.hash(password)
        return '', True

    def generate_token(self):
        """
        Generate the access token
        :return:
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': self.id
            }

            jwt_string = jwt.encode(
                payload, current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )

            return jwt_string
        except Exception as ex:
            return str(ex)

    @staticmethod
    def decode_token(token):
        """
        Decode the access token from the Authorization header
        :param token:
        :return:
        """
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Expired token'
        except jwt.InvalidTokenError:
            return 'Invalid token'

    def __init__(self, name):
        self.name = name


ma = MarshmallowInstance.get()


class UserSchema(ma.Schema):
    """
    Schema of User
    """
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(3))
    url = ma.URLFor('auth_api.userresource', identifier='<id>', _external=True)
