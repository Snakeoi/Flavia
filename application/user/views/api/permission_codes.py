from flask import views
from flask import jsonify

from application.models import PermissionCodes


class PermissionCodesView(views.MethodView):
    def get(self):
        return jsonify(PermissionCodes.LISTED)
