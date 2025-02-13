from flask_login import current_user
from application.extensions import db


def update_user_last_seen():
    if not current_user.is_anonymous:
        current_user.last_seen = db.func.now()
        db.session.commit()
