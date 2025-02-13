from application.utils.schema_serialization import serialize_schema
from ...schemas import UserCreateSchema, UserUpdateSchema
from flask import views, jsonify


class UserCreateSchemaView(views.MethodView):
    def get(self):
        return jsonify(serialize_schema(UserCreateSchema()))


class UserUpdateSchemaView(views.MethodView):
    def get(self):
        return jsonify(serialize_schema(UserUpdateSchema()))
