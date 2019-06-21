# app/message_blueprint/models.py

from marshmallow import fields, pre_load, validate
from app.__common import DbInstance, MarshmallowInstance, AddUpdateDelete

db = DbInstance.get()
ma = MarshmallowInstance.get()


class Category(db.Model, AddUpdateDelete):
    """
    Category Model
    """
    __tablename__ = 't_signal_message_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    @classmethod
    def is_exist(cls, identifier, name):
        """
        Check if the category_name & category_identifier is existing or not
        :param identifier: category's identifier
        :param name: category's name
        :return: True if existed, else False
        """
        existing_category = cls.query.filter_by(name=name).first()
        if existing_category is None:
            return False
        else:
            if existing_category.id == identifier:
                return False
            else:
                return True


class Message(db.Model, AddUpdateDelete):
    """
    Message Model
    """
    __tablename__ = 't_signal_messages'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(250), unique=True, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('{table}.id'.format(table=Category.__tablename__), ondelete='CASCADE'),
                            nullable=False)
    category = db.relationship('Category', backref=db.backref('messages', lazy='dynamic', order_by='Message.message'))
    printed_times = db.Column(db.Integer, nullable=False, server_default='0')
    printed_once = db.Column(db.Boolean, nullable=False, server_default='0')

    def __init__(self, message, duration, category):
        self.message = message
        self.duration = duration
        self.category = category

    @classmethod
    def is_exist(cls, identifier, message):
        """
        Check if the message_message & message_identifier is existing or not
        :param identifier: message' identifier
        :param message: message's message
        :return: True if existed, else False
        """
        existing_message = cls.query.filter_by(message=message).first()

        if existing_message is None:
            return False
        else:
            if existing_message.id == identifier:
                return False
            else:
                return True


class CategorySchema(ma.Schema):
    """
    Category Schema
    """

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(3))
    url = ma.URLFor('signal_api.categoryresource', identifier='<id>', _external=True)
    messages = fields.Nested('MessageSchema', many=True, exclude=('category',))


class MessageSchema(ma.Schema):
    """
    Message Schema
    """
    id = fields.Integer(dump_only=True)
    message = fields.String(required=True, validate=validate.Length(1))
    duration = fields.Integer()
    creation_date = fields.DateTime()
    category = fields.Nested(CategorySchema, only=['id', 'url', 'name'], required=True)
    printed_times = fields.Integer()
    printed_once = fields.Boolean()

    url = ma.URLFor('signal_api.messageresource', identifier='<id>', _external=True)

    @pre_load
    def process_category(self, data):
        category = data.get('category')

        if category:
            if isinstance(category, dict):
                category_name = category.get('name')
            else:
                category_name = category

            category_dict = dict(name=category_name)
        else:
            category_dict = {}

        data['category'] = category_dict
        return data
