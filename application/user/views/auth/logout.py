from flask import views, flash, redirect, url_for
from flask_login import logout_user


class LogoutView(views.MethodView):
    def get(self):
        logout_user()
        flash("You have been logged out.", category="success")
        return redirect(url_for("user_auth.login"))
