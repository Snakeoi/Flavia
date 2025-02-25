import pytest
from flask import current_app
from werkzeug.exceptions import NotFound

from tests.fixtures.app_fixtures import app

from application.models import User
from application.extensions import db
from application.user.views.auth.register import send_confirmation_email

def send_email_mock(email, subject, template, **kwargs):
    pass

class TestSendConfirmationEmail:

    def setup_method(self):
        with app.app_context():
            db.create_all()

    def test_send_confirmation_email_raises_type_error_if_user_and_email_are_both_none(self):
        with app.app_context():
            with pytest.raises(TypeError):
                send_confirmation_email(
                    user=None,
                    email=None,
                    email_sender_func=send_email_mock
                )

    def test_send_confirmation_email_raises_not_found_error_while_user_by_email_not_exist(self):
        with app.app_context():
            with pytest.raises(NotFound):
                send_confirmation_email(
                    email='not_existing_buddy@example.com',
                    email_sender_func=send_email_mock
                )

    def test_send_confirmation_email_sends_email_to_user_email_by_email(self):
        with app.app_context():
            db.session.add(User(
                email='buddy@example.com',
                username='John Doe',
            ))
            db.session.commit()

            send_confirmation_email(
                email='buddy@example.com',
                email_sender_func=send_email_mock
            )

    def test_send_confirmation_email_sends_email_to_user_email_by_user_object(self):
        with app.app_context():
            db.session.add(User(
                email='buddy@example.com',
                username='John Doe',
            ))
            db.session.commit()

            send_confirmation_email(
                user=User,
                email_sender_func=send_email_mock
            )

    def teardown_method(self):
        with app.app_context():
            db.drop_all()

def test_everyone_can_register_is_off_returns_404():
    with app.test_request_context():
        app.config["EVERYONE_CAN_REGISTER"] = False
        with app.test_client() as client:
            response = client.get("/user/register")
            assert response.status_code == 404

def test_get_renders_registration_form():
    with app.test_request_context():
        current_app.config["EVERYONE_CAN_REGISTER"] = True
        with app.test_client() as client:
            response = client.get("/user/register")
            assert response.status_code == 200

class TestPost:

    def setup_method(self):
        with app.app_context():
            db.create_all()

    def test_post_with_existing_email_shows_error(self):
        with app.test_request_context():
            with app.test_client() as client:
                user = User(email="test@example.com", username="testuser", password="password")
                db.session.add(user)
                db.session.commit()
                response = client.post("/user/register", data={"email": "test@example.com", "username": "newuser", "password": "as1EDF^&(HHG>", "password2": "as1EDF^&(HHG>"})
                assert b"Email already in use." in response.data

    def test_post_with_valid_data_creates_user_and_sends_email(self):
        with app.test_request_context():
            current_app.config["EVERYONE_CAN_REGISTER"] = True
            with app.test_client() as client:
                response = client.post("/user/register",
                                       data={"email": "test@example.com", "username": "newuser", "password": "as1EDF^&(HHG>", "password2": "as1EDF^&(HHG>"})
                assert response.status_code == 302

    def test_post_with_invalid_data_shows_errors(self):
        with app.test_request_context():
            current_app.config["EVERYONE_CAN_REGISTER"] = True
            with app.test_client() as client:
                response = client.post("/user/register", data={"email": "invalid", "username": "", "password": "as1EDF^&(HHG>", "password2": "as1EDF^&(HHG>"})
                assert b"Must be valid email address." in response.data

    def teardown_method(self):
        with app.app_context():
            db.drop_all()