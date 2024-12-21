from functools import wraps

from flask import abort, jsonify
from flask_login import login_required, current_user
from flask_login.mixins import AnonymousUserMixin
from marshmallow import ValidationError


def permission_required(*permissions: str):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            if current_user.have_permission(*permissions):
                return func(*args, **kwargs)
            else:
                abort(403)
        return wrapper
    return decorator


def permission_required_api(*permissions: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(current_user, func.__name__)
            if isinstance(current_user, AnonymousUserMixin):
                abort(401)
            else:
                if current_user.have_permission(*permissions):
                    return func(*args, **kwargs)
                else:
                    abort(403)
        return wrapper
    return decorator


def handle_ma_validation_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as err:
            errors = []
            for field, messages in err.messages.items():
                for message in messages:
                    errors.append(f"{field}: {message}")
            return jsonify({"errors": errors}), 400
    return wrapper
