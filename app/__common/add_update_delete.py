import sys
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


class DbInstance:
    """
    Singleton class to create instance of SQLAlchemy
    """
    _db = None

    @classmethod
    def get(cls) -> SQLAlchemy:
        if cls._db is None:
            cls._db = SQLAlchemy()

        return cls._db


class MarshmallowInstance:
    """
    Singleton class to create instance of Marshmallow
    """
    _ma = None
    @classmethod
    def get(cls) -> Marshmallow:
        if cls._ma is None:
            cls._ma = Marshmallow()

        return cls._ma


class AddUpdateDelete:
    """
    Base class provided the action of adding, updating and deleting
    """

    db = DbInstance.get()

    def add(self, resource):
        self.db.session.add(resource)
        self.db.session.commit()

    def update(self):
        self.db.session.commit()

    def delete(self, resource):
        self.db.session.delete(resource)
        self.db.session.commit()
