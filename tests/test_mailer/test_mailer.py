import pytest

from application.mailer import send_email
from application.models import User

from ..fixtures.app_fixtures import app


def send_async_email_mockup(app, msg):
    pass

user = User(
    email='john.doe@example.com',
    username='John Doe',
    password='P@ssw0rd'
)

@pytest.mark.parametrize(
    "to, subject, template, kwargs",
    [
        ('1@example.com', 'subject', 'user/confirm', {"user": user}),
        ('2@example.com', 'subject', 'user/reset', {"user": user}),
    ]
)
def test_send_email_sends_email_to_recipient(to, subject, template, kwargs):
    with app.test_request_context():
        send_email(
            to=to,
            subject=subject,
            template=template,
            sender=send_async_email_mockup,
            **kwargs
        )