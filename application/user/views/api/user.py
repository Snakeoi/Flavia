from flask import views, jsonify, request
from flask_login import current_user

from application.models import User, PermissionCodes, Permission
from ..auth.register import send_confirmation_email
from ...schemas import UserReadSchema, UserCreateSchema, UserUpdateSchema
from application.utils.decorators import permission_required_api, handle_ma_validation_errors
from application.extensions import db


class PermissionsSetupHandler:
    def list_permission_codes(self, permission_codes: dict[str]) -> list[str]:
        return [permission["codename"] for permission in permission_codes]

    def add_permissions(self, user: "User", permission_codes: dict[str]):
        permission_codes = self.list_permission_codes(permission_codes)
        for permission in permission_codes:
            if permission in PermissionCodes.LISTED and permission not in user.permissions_list:
                db.session.add(
                    Permission(
                        user_id=user.id,
                        codename=permission,
                    )
                )

    def remove_permissions(self, user: "User", permission_codes: dict[str]):
        permission_codes = self.list_permission_codes(permission_codes)
        for permission in user.permissions_list:
            if permission not in permission_codes:
                db.session.delete(
                    Permission.query.filter_by(
                        user_id=user.id,
                        codename=permission,
                    ).first_or_404()
                )


class UsersView(views.MethodView, PermissionsSetupHandler):
    decorators = [permission_required_api(PermissionCodes.ADMIN), handle_ma_validation_errors]

    def get(self):
        return jsonify(UserReadSchema(many=True).dump(User.query.all()))

    def post(self):
        data: dict = UserCreateSchema().load(request.get_json())

        if User.query.filter_by(email=data["email"].lower()).first():
            return jsonify({"errors": ["Email already in use."]}), 400

        user: "User" = User(email=data["email"].lower(), username=data["username"].strip(), password=data["password"])
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=data["email"].lower()).first()
        self.add_permissions(user, data["permissions"])
        db.session.commit()

        if data["send_confirmation_email"]:
            send_confirmation_email(user=user)

        return jsonify(UserReadSchema().dump(user)), 201


class SendConfirmationEmailView(views.MethodView):
    decorators = [
        permission_required_api(PermissionCodes.ADMIN),
    ]

    def post(self, user_id: int):
        user: "User" = User.query.get_one(user_id)
        if not user.confirmed:
            send_confirmation_email(user=user)
            return jsonify(), 202
        else:
            return jsonify({"errors": ["User is already confirmed."]}), 409


class UserView(views.MethodView, PermissionsSetupHandler):
    decorators = [permission_required_api(PermissionCodes.ADMIN), handle_ma_validation_errors]

    def get(self, user_id: int):
        return jsonify(UserReadSchema().dump(User.query.get_or_404(user_id)))

    def patch(self, user_id: int):
        data: dict = UserUpdateSchema().load(request.get_json())
        user: "User" = User.query.get_or_404(user_id)

        if 'permissions' in data.keys():
            permission_codes = self.list_permission_codes(data["permissions"])
            if PermissionCodes.ADMIN not in permission_codes:
                return jsonify({"errors": ["You cannot remove admin permission from yourself."]}), 400

        for key in data.keys():
            if key == "permissions":
                self.add_permissions(user, data["permissions"])
                self.remove_permissions(user, data["permissions"])
            else:
                setattr(user, key, data[key])

        db.session.commit()
        return jsonify(UserReadSchema().dump(user))

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        if user_id == current_user.id:
            return jsonify({"errors": ["You cannot delete yourself."]}), 400
        db.session.delete(user)
        db.session.commit()
        return jsonify(), 204
