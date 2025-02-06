import pytest
from sqlalchemy import inspect

from .fixtures.app_fixtures import app
from application.extensions import db

class TestModelsCreation:

    def setup_method(self):
        with app.app_context():
            db.create_all()
            inspector = inspect(db.engine)
            self.table_names = inspector.get_table_names()

    def test_models_creation_in_database(self):
        assert self.table_names == [
            'agreements',
            'permissions',
            'users',
        ]

    def teardown_method(self):
        with app.app_context():
            db.drop_all()