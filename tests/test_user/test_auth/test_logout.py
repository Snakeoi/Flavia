from flask_login import login_user, current_user

from tests.fixtures.app_fixtures import DatabaseCreateDropFixture
from tests.fixtures.make_user import make_user

from tests.fixtures.app_fixtures import app

class TestLogout(DatabaseCreateDropFixture):

    def test_logout(self):
        with app.test_request_context():
            with app.test_client() as client:
                user = make_user()
                login_user(user)
                client.get("/user/logout")
                assert current_user.is_authenticated is False