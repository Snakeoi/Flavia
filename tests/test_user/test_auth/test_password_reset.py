from application.models import User
from application.extensions import db
from tests.fixtures.make_user import make_user
from tests.fixtures.app_fixtures import DatabaseCreateDropFixture

from tests.fixtures.app_fixtures import app


class TestPasswordReset(DatabaseCreateDropFixture):

    def test_reset_password_form_appears(self):
        with app.test_request_context():
            with app.test_client() as client:
                response = client.get("/user/reset_password")
                assert response.status_code == 200
                assert b"Reset Password" in response.data

    def test_send_reset_email_to_existing_user(self):
        with app.test_request_context():
            with app.test_client() as client:
                user = User(email="test@example.com", username="testuser", password="password")
                db.session.add(user)
                db.session.commit()
                response = client.post("/user/reset_password", json={"email": "test@example.com"})
                assert response.status_code == 200

    def test_send_reset_email_to_non_existing_user_returns_success(self):
        with app.test_request_context():
            with app.test_client() as client:
                response = client.post("/user/reset_password", json={"email": "nonexistent@example.com"})
                assert response.status_code == 200
                assert b"No email found." in response.data

    def test_reset_password_with_valid_pin_changes_password(self):
        with app.test_request_context():
            with app.test_client() as client:
                user = User(email="test@example.com", username="testuser", password="0ld_p@ssw0rd")
                db.session.add(user)
                db.session.commit()
                pin = user.set_reset_password_pin()
                response = client.post("/user/reset_password",
                                       data={
                                           "email": "test@example.com",
                                           "pin": pin,
                                           "password": "New_p@ssw0rd",
                                           "password2": "New_p@ssw0rd"
                                       })
                assert response.status_code == 302
                assert user.verify_password("New_p@ssw0rd") is True

    def test_reset_password_with_invalid_pin_shows_error(self):
        with app.test_request_context():
            with app.test_client() as client:
                user = User(email="test@example.com", username="testuser", password="oldpassword")
                db.session.add(user)
                db.session.commit()
                pin = user.set_reset_password_pin()

                invalid_pin = pin[:-1] + "9"

                response = client.post("/user/reset_password",
                                       data={
                                           "email": "test@example.com",
                                           "pin": invalid_pin,
                                           "password": "New_p@ssw0rd",
                                           "password2": "New_p@ssw0rd"
                                       })
                assert response.status_code == 200
                assert b"Invalid PIN" in response.data

    def test_reset_password_with_non_existing_email_shows_error(self):
        with app.test_request_context():
            with app.test_client() as client:
                response = client.post("/user/reset_password",
                                       data={"email": "nonexistent@example.com", "pin": "123456",
                                             "password": "newpassword"})
                assert response.status_code == 200
                assert b"No email found." in response.data

    def test_send_reset_email_with_pin_for_existing_user(self):
        with app.test_request_context():
            with app.test_client() as client:
                user = make_user()
                response = client.post("/user/send_reset", json={"email": user.email})
                assert response.status_code == 200
                assert response.json == {"msg": "Password reset email has been send to user email."}

    def test_send_reset_email_with_pin_for_non_existing_user_is_false_positive(self):
        with app.test_request_context():
            with app.test_client() as client:
                response = client.post("/user/send_reset", json={"email": "some.guy@example.com"})
                assert response.status_code == 200
                assert response.json == {"msg": "Password reset email has been send to user email."}

    def test_send_reset_email_with_pin_with_invalid_email(self):
        with app.test_request_context():
            with app.test_client() as client:
                response = client.post("/user/send_reset", json={"email": "invalid_email"})
                assert response.status_code == 400
                assert response.json == {'email': ['Must be valid email address.']}

    def test_send_reset_email_with_pin_with_wrong_request_data(self):
        with app.test_request_context():
            with app.test_client() as client:
                response = client.post("/user/send_reset", json={"invalid_field": "invalid_value"})
                assert response.status_code == 400
                assert response.json == {'email': ['Missing data for required field.'],
                                         'invalid_field': ['Unknown field.']}
