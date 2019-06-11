# app/message_blueprint/category_resources.py

from flask import jsonify, make_response, url_for
from flask_restful import Resource, request, marshal_with
from .signal_models import CategorySchema, Category, db
from app.__common import HttpStatus, PaginationHelper, AuthRequiredResource
from sqlalchemy.exc import SQLAlchemyError
from app.app_factory import __create_logger

logger = __create_logger()


class CategoryResource(AuthRequiredResource):
    __category_schema: CategorySchema = CategorySchema()

    def get(self, identifier):
        category = Category.query.get_or_404(identifier)
        result = self.__category_schema.dump(category).data
        return result

    def patch(self, identifier):
        category = Category.query.get_or_404(identifier)
        category_dict = request.get_json()
        if not category_dict:
            resp = {'message': 'No input data provided'}
            return resp, HttpStatus.HTTP_400_BAD_REQUEST

        errors = self.__category_schema.validate(category_dict)
        if errors:
            return errors, HttpStatus.HTTP_400_BAD_REQUEST

        try:
            if 'name' in category_dict:
                category_name = category_dict['name']
                if not Category.is_exist(identifier=identifier, name=category_name):
                    category.name = category_name
                else:
                    response = {'error': 'A category with the same name already exists'}
                    return response, HttpStatus.HTTP_400_BAD_REQUEST

            category.update()
            return self.get(identifier)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, HttpStatus.HTTP_400_BAD_REQUEST

    def delete(self, identifier):
        category = Category.query.get_or_404(identifier)

        try:
            category.delete(category)
            return HttpStatus.HTTP_204_NO_CONTENT, {'Location': url_for('signal_api.categorylistresource.')}
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, HttpStatus.HTTP_401_UNAUTHORIZED


class CategoryListResource(AuthRequiredResource):
    __category_schema: CategorySchema = CategorySchema()

    def get(self):
        categories = Category.query.all()
        results = self.__category_schema.dump(categories, many=True).data
        return results

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            resp = {'message': 'No input data provided'}
            logger.debug(resp)
            return resp, HttpStatus.HTTP_400_BAD_REQUEST

        errors = self.__category_schema.validate(request_dict)
        if errors:
            logger.debug(errors)
            return errors, HttpStatus.HTTP_400_BAD_REQUEST

        category_name = request_dict['name']
        if Category.is_exist(identifier=0, name=category_name):
            logger.debug('A category with the same name already exists')
            response = {'error': 'A category with the same name already exists'}
            return response, HttpStatus.HTTP_400_BAD_REQUEST

        try:
            category = Category(category_name)
            category.add(category)
            query = Category.query.get(category.id)
            result = self.__category_schema.dump(query).data

            return result, HttpStatus.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, HttpStatus.HTTP_400_BAD_REQUEST
