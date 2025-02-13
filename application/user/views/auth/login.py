from flask import request, views, current_app, render_template, url_for, redirect, flash
from flask_login import login_user

from application.models import User
from .register import send_confirmation_email

from application.user.forms import LoginForm


class LoginView(views.MethodView):
    def get(self):
        form = LoginForm()
        return render_template("user/login.html", form=form)

    def post(self):
        form = LoginForm()
        if form.validate_on_submit() or current_app.config["MODE"] == "development":
            user: "User" = User.query.filter_by(email=form.email.data.lower()).first()

            if user is not None and user.verify_password(form.password.data):
                if not user.confirmed:
                    flash(
                        "The account is unconfirmed. The verification email has been resent to the address provided.",
                        category="warning",
                    )
                    send_confirmation_email(email=user.email)
                elif not user.is_active:
                    flash("Your account has been deactivated.", category="danger")
                else:
                    login_user(user, form.remember_me.data)
                    next_view = request.args.get("next")
                    if next_view is None or not next_view.startswith("/"):
                        next_view = url_for("vue.index")
                    return redirect(next_view)
            else:
                flash("Invalid email or password.", category="danger")
        return render_template("user/login.html", form=form)
