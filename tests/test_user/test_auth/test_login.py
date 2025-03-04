from flask import url_for, current_app

from application.models import User
from application.extensions import db
from tests.fixtures.app_fixtures import DatabaseCreateDropFixture

from tests.fixtures.app_fixtures import app


class TestLogin(DatabaseCreateDropFixture):

    def test_login_with_valid_credentials_redirects_to_index(self):
        with app.test_request_context():
            with app.test_client() as client:
                user = User(email="test@example.com", username="testuser", password="password", confirmed=True,
                            is_active=True)
                db.session.add(user)
                db.session.commit()
                response = client.post("/user/login",
                                       data={"email": "test@example.com", "password": "password", "remember_me": False})
                assert response.status_code == 302
                assert response.location.endswith(url_for("vue.index"))

    def test_login_with_unconfirmed_account_resends_confirmation_email(self):
        with app.test_request_context():
            with app.test_client() as client:
                user = User(email="test@example.com", username="testuser", password="P@ssw0rd", confirmed=False)
                db.session.add(user)
                db.session.commit()
                response = client.post("/user/login", data={"email": "test@example.com", "password": "P@ssw0rd"})
                assert response.status_code == 200
                assert b"The account is unconfirmed. The verification email has been resent to the address provided." in response.data

    def test_login_with_deactivated_account_shows_error(self):
        with app.test_request_context():
            with app.test_client() as client:
                user = User(email="test@example.com", username="testuser", password="password", confirmed=True,
                            is_active=False)
                db.session.add(user)
                db.session.commit()
                response = client.post("/user/login", data={"email": "test@example.com", "password": "password"})
                assert response.status_code == 200
                assert b"Your account has been deactivated." in response.data

    def test_login_with_invalid_credentials_shows_error(self):
        with app.test_request_context():
            with app.test_client() as client:
                user = User(email="test@example.com", username="testuser", password="password", confirmed=True,
                            is_active=True)
                db.session.add(user)
                db.session.commit()
                response = client.post("/user/login", data={"email": "test@example.com", "password": "wrongpassword"})
                assert response.status_code == 200
                assert b"Invalid email or password." in response.data

    def test_login_with_valid_credentials_in_development_mode(self):
        with app.test_request_context():
            with app.test_client() as client:
                current_app.config["MODE"] = "development"
                response = client.post("/user/login", data={"email": "test@example.com", "password": "password"})
                assert response.status_code == 200
