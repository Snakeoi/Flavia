import os

from dotenv import load_dotenv
from flask import Flask

from .config import assignment
from .extensions import setup_extensions
from .injects import setup_injects
from .blueprints import setup_blueprints
from . import utils
from .middleware import update_user_last_seen

load_dotenv()


def create_app():

    app = Flask(__name__)
    app.config.from_object(
        assignment[os.environ.get('MODE', 'production')]
    )

    setup_extensions(app)

    setup_injects(app)

    @app.before_request
    def after_request():
        update_user_last_seen()

    setup_blueprints(app, {
        'vue': ('vue',),
        'user': ('user_auth', 'user_api'),
    })

    app.add_url_rule('/map', view_func=utils.map.view)

    return app
