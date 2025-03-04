from application.models import User
from application.extensions import db
from tests.fixtures.app_fixtures import DatabaseCreateDropFixture

from tests.fixtures.app_fixtures import app

class TestPasswordReset(DatabaseCreateDropFixture):


    def test_confirm_view_with_valid_token_confirms_user(self):
        with app.test_request_context():
            with app.test_client() as client:
                user = User(email="test@example.com", username="testuser", password="password")
                db.session.add(user)
                db.session.commit()
                token = user.generate_confirmation_token()
                response = client.get(f"/user/confirm/{token}")
                assert response.status_code == 200
                assert b"Account is confirmed!" in response.data

    def test_confirm_view_with_invalid_token_shows_error(self):
        with app.test_request_context():
            with app.test_client() as client:
                response = client.get("/user/confirm/expiredtoken")
                assert response.status_code == 200
                assert b"Token has expired or is invalid." in response.data

    def test_confirm_view_with_non_existing_user_shows_error(self):
        with app.test_request_context():
            with app.test_client() as client:
                user = User(email="test@example.com", username="testuser", password="password")
                token = user.generate_confirmation_token()
                # We are not adding the user to the database

                response = client.get(f"/user/confirm/{token}")
                assert response.status_code == 200
                assert b"Token has expired or is invalid." in response.data