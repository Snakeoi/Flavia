import pytest

from application import create_app
from application.extensions import db

app = create_app('testing')

@pytest.fixture
def app_db_create_destroy():
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()