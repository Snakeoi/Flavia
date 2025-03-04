from flask_login import login_user

from tests.fixtures.app_fixtures import app
from tests.fixtures.app_fixtures import DatabaseCreateDropFixture
from tests.fixtures.make_user import make_user


class TestCurrentUser(DatabaseCreateDropFixture):

    def test_current_user_view_returns_current_user(self):
        with app.test_request_context():
            with app.test_client() as client:
                user = make_user()
                login_user(user)
                response = client.get("/api/user/current")
                assert response.status_code == 200
                assert response.json['confirmed'] is False
                assert response.json['email'] == 'john.doe@example.com'
                assert response.json['id'] == 1
                assert response.json['permissions'] == []
                assert response.json['username'] == 'John Doe'
                assert response.json.keys() == {'confirmed', 'email', 'id', 'last_seen', 'member_since', 'permissions',
                                                'username'}
