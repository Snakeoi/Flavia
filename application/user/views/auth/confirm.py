from flask import views, render_template
from flask_jwt_extended import decode_token
from jwt import ExpiredSignatureError, InvalidTokenError

from application.extensions import db
from application.models import User


class ConfirmView(views.MethodView):
    def get(self, token):
        try:
            decoded = decode_token(token)
            user = User.query.filter_by(email=decoded["sub"]).first()
            if user is None:
                raise InvalidTokenError()

            if user.confirm(token):
                db.session.commit()
                success = True
            else:
                raise InvalidTokenError()

        except (ExpiredSignatureError, InvalidTokenError):
            success = False

        return render_template("user/confirmed.html", success=success)
