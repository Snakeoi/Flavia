from flask import jsonify, request, views, render_template, flash, redirect, url_for
from marshmallow import ValidationError
from application.mailer import send_email

from application.user.forms import PasswordResetForm
from application.models import User
from application.user.schemas import EmailSchema


def send_password_reset_email_with_pin(user, pin):
    send_email(user.email, "Reset your password", "user/reset", user=user, pin=pin)


class SendResetEmailView(views.MethodView):
    def response(self):
        return jsonify({"msg": "Password reset email has been send to user email."}), 200

    def post(self):
        json_input = request.get_json()
        change_password_schema = EmailSchema()
        try:
            data = change_password_schema.load(json_input)
        except ValidationError as err:
            return jsonify(err.messages), 400

        user = User.query.filter_by(email=data["email"]).first()
        if user is None:
            return self.response()

        send_password_reset_email_with_pin(user, pin=user.set_reset_password_pin())

        return self.response()


class ResetPasswordView(views.MethodView):
    def get(self):
        form = PasswordResetForm()
        return render_template("user/reset_password.html", form=form)

    def post(self):
        form = PasswordResetForm()

        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None:
            flash("No email found.", "warning")
        elif form.validate_on_submit():
            if user.reset_password(pin=form.pin.data, new_password=form.password.data):
                flash("Password has been changed.", "success")
                return redirect(url_for("user_auth.login"))
            else:
                flash("Invalid PIN", "danger")
        else:
            for field in form.errors.values():
                for error in field:
                    flash(error, "danger")

        return render_template("user/reset_password.html", form=form)
