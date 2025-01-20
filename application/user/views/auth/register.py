from flask import views, abort, flash, redirect, render_template, url_for, current_app

from application.extensions import db
from application.mailer import send_email

from application.user.forms import RegistrationForm
from application.models import User


def send_confirmation_email(email=None, user=None):
    if user is None and email is None:
        raise TypeError('At least one argument cannot be None')

    if user is None:
        user = User.query.filter_by(email=email).first_or_404()

    send_email(
        user.email,
        'Confirm your account',
        'user/confirm',
        user=user
    )


class RegisterView(views.MethodView):

    def _block_if_off(self):
        if not current_app.config['EVERYONE_CAN_REGISTER']:
            return abort(404)

    def get(self):
        self._block_if_off()

        form = RegistrationForm()
        return render_template('user/register.html', form=form)

    def post(self):
        self._block_if_off()

        form = RegistrationForm()
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash('Email already in use.', 'danger')
        else:
            if form.validate_on_submit():
                user = User(
                    email=form.email.data.lower(),
                    username=form.username.data.strip(),
                    password=form.password.data,
                    is_active=False
                )
                db.session.add(user)
                db.session.commit()
                send_confirmation_email(user=user)
                flash('A confirmation email has been sent to you by email.', 'info')
                return redirect(url_for('user_auth.login'))
            else:
                for field in form.errors.values():
                    for error in field:
                        flash(error, 'danger')

        return render_template('user/register.html', form=form)
