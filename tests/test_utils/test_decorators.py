import pytest
from werkzeug.exceptions import Forbidden
from werkzeug.exceptions import Unauthorized
from flask_login import UserMixin
from flask_login import AnonymousUserMixin
from flask_login import login_user
from marshmallow import ValidationError

from application.utils.decorators import permission_required
from application.utils.decorators import permission_required_api
from application.utils.decorators import handle_ma_validation_errors

from ..fixtures.app_fixtures import app


class MockUser(UserMixin):
    def __init__(self, permissions):
        self.id = 1
        self.permissions = permissions

    def have_permission(self, *permissions):
        return all(permission in self.permissions for permission in permissions)


def test_permission_required_decorator_allows_access_to_authorized_user():
    user = MockUser(permissions=["read"])
    with app.test_request_context():
        login_user(user)

        @permission_required("read")
        def view():
            return "success"

        assert view() == "success"


def test_permission_required_decorator_denies_access_to_unauthorized_user():
    user = MockUser(permissions=[])

    with app.test_request_context():
        login_user(user)

        @permission_required("read")
        def view():
            return "success"

        with pytest.raises(Forbidden):
            assert view()


def test_permission_required_api_decorator_allows_access_to_authorized_user():
    user = MockUser(permissions=["read"])
    with app.test_request_context():
        login_user(user)

        @permission_required_api("read")
        def view():
            return "success"

        assert view() == "success"


def test_permission_required_api_decorator_denies_access_to_unauthorized_user():
    user = MockUser(permissions=[])

    with app.test_request_context():
        login_user(user)

        @permission_required_api("read")
        def view():
            return "success"

        with pytest.raises(Forbidden):
            assert view()


def test_permission_required_api_decorator_denies_access_to_anonymous_user():
    user = AnonymousUserMixin()

    with app.test_request_context():
        login_user(user)

        @permission_required_api("read")
        def view():
            return "success"

        with pytest.raises(Unauthorized):
            assert view()


def test_handle_ma_validation_errors_decorator_handles_validation_error():
    with app.app_context():

        @handle_ma_validation_errors
        def view():
            raise ValidationError({"field": ["invalid"]})

        response = view()
        assert response[1] == 400
        assert response[0].json == {"errors": ["field: invalid"]}
