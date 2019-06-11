import re

from marshmallow import validate, fields
from passlib.apps import custom_app_context as password_context

from app.__common import DbInstance, MarshmallowInstance, AddUpdateDelete

db = DbInstance.get()


class User(db.Model, AddUpdateDelete):
    """
    Model of User
    """
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
