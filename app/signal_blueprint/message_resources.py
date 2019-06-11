# app/message_blueprint/message_resources.py

from flask import request, jsonify, make_response, url_for
from flask_restful import Resource, marshal_with
from .signal_models import Message, MessageSchema, Category, CategorySchema
from app.__common import DbInstance, HttpStatus, PaginationHelper, AuthRequiredResource
from sqlalchemy.exc import SQLAlchemyError

db = DbInstance.get()


class MessageResource(AuthRequiredResource):
    __message_schema: MessageSchema = MessageSchema()

    def get(self, identifier):
        message = Message.query.get_or_404(identifier)
        result = self.__message_schema.dump(message).data
        return result

    def patch(self, identifier):
        message = Message.query.get_or_404(identifier)
        message_dict = request.get_json(force=True)

        if 'message' in message_dict:
            message_message = message_dict['message']
            if not Message.is_exist(identifier=identifier, message=message_message):
                message.message = message_message
            else:
                response = {'error': 'A message with the same message already exists'}
                return response, HttpStatus.HTTP_400_BAD_REQUEST

        if 'duration' in message_dict:
            try:
                message.duration = int(message_dict['duration'])
            except ValueError:
                response = {'error': 'Field [duration] must be integer'}
                return response, HttpStatus.HTTP_400_BAD_REQUEST

        if 'printed_times' in message_dict:
            try:
                message.printed_times = int(message_dict['printed_times'])
            except ValueError:
                response = {'error': 'Field [printed_times] must be integer'}
                return response, HttpStatus.HTTP_400_BAD_REQUEST

        if 'printed_once' in message_dict:
            message.printed_once = True if str(message_dict['printed_once']).strip().lower() == 'true' else False

        dumped_message, dump_errors = self.__message_schema.dump(message)
        if dump_errors:
            return dump_errors, HttpStatus.HTTP_400_BAD_REQUEST

        validate_errors = self.__message_schema.validate(dumped_message)
        if validate_errors:
            return validate_errors, HttpStatus.HTTP_400_BAD_REQUEST

        try:
            message.update()
            return self.get(identifier=identifier)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, HttpStatus.HTTP_400_BAD_REQUEST

    def delete(self, identifier):
        message = Message.query.get_or_404(identifier)

        try:
            message.delete(message)
            return HttpStatus.HTTP_204_NO_CONTENT, {'Location': url_for('signal_api.categorylistresource.')}
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, HttpStatus.HTTP_401_UNAUTHORIZED


class MessageListResource(AuthRequiredResource):
    __message_schema: MessageSchema = MessageSchema()

    def get(self):
        pagination_helper = PaginationHelper(
            request,
            query=Message.query,
            resource_for_url='signal_api.messagelistresource',
            key_name='results',
            schema=self.__message_schema)

        result = pagination_helper.paginate_query()
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {'message': 'No input data provided'}
            return response, HttpStatus.HTTP_400_BAD_REQUEST

        errors = self.__message_schema.validate(request_dict)
        if errors:
            return errors, HttpStatus.HTTP_400_BAD_REQUEST

        message_message = request_dict['message']
        if Message.is_exist(identifier=0, message=message_message):
            response = {'error': 'A message with the same message already exists'}
            return response, HttpStatus.HTTP_400_BAD_REQUEST

        try:
            category_name = request_dict['category']['name']
            category = Category.query.filter_by(name=category_name).first()

            if category is None:
                # Create a new Category
                category = Category(name=category_name)
                db.session.add(category)

            # Now that we are sure we have a category
            # create a new Message
            message = Message(
                message=message_message,
                duration=request_dict['duration'],
                category=category)
            message.add(message)

            query = Message.query.get(message.id)
            result = self.__message_schema.dump(query).data

            return result, HttpStatus.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, HttpStatus.HTTP_400_BAD_REQUEST
