from flask import views, jsonify, abort

from flask_login import current_user

from application.user.schemas import UserReadSchema
from application.utils import permission_required_api


class CurrentUserView(views.MethodView):
    decorators = [permission_required_api()]

    def get(self):
        schema = UserReadSchema()
        schema_data = schema.dump(current_user)
        return jsonify(schema_data)
