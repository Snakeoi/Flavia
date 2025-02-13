"""Initialize any app extensions."""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_login import LoginManager

cors = CORS(resources={r"/*": {"origins": "*"}}, supports_credentials=True)

db = SQLAlchemy()

ma = Marshmallow()

mail = Mail()

jwt = JWTManager()

migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = "user_auth.login"


def setup_extensions(app):
    app.json.ensure_ascii = False

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    login_manager.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
