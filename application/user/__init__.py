from flask import Blueprint

from application.extensions import jwt

from . import views
from application.models import User


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(email=identity).one_or_none()


user_auth = Blueprint(
    'user_auth',
    __name__,
    url_prefix='/user',
    template_folder='templates'
)

user_auth.add_url_rule('/login', view_func=views.auth.LoginView.as_view('login'))
user_auth.add_url_rule('/logout', view_func=views.auth.LogoutView.as_view('logout'))
user_auth.add_url_rule('/register', view_func=views.auth.RegisterView.as_view('register'))
user_auth.add_url_rule('/confirm/<token>', view_func=views.auth.ConfirmView.as_view('confirm'))
user_auth.add_url_rule('/send_reset', view_func=views.auth.SendResetEmailView.as_view('send_reset'))
user_auth.add_url_rule('/reset_password', view_func=views.auth.ResetPasswordView.as_view('reset_password'))


user_api = Blueprint(
    'user_api',
    __name__,
    url_prefix='/api/user',
)

user_api.add_url_rule('/', view_func=views.api.UsersView.as_view('users'))
user_api.add_url_rule('/schema/create', view_func=views.api.UserCreateSchemaView.as_view('create-schema'))
user_api.add_url_rule('/schema/update', view_func=views.api.UserUpdateSchemaView.as_view('update-schema'))
user_api.add_url_rule('/<int:user_id>', view_func=views.api.UserView.as_view('user'))
user_api.add_url_rule('/current', view_func=views.api.CurrentUserView.as_view('current'))
user_api.add_url_rule('/permission-codes', view_func=views.api.PermissionCodesView.as_view('permission_codes'))
user_api.add_url_rule(
    '/send_confirmation_email/<int:user_id>',
    view_func=views.api.SendConfirmationEmailView.as_view('send_confirmation_email')
)
