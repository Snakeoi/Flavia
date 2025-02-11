import pytest
from sqlalchemy import inspect

from .fixtures.app_fixtures import app
from application.extensions import db

class TestModelsCreation:

    def setup_method(self):
        with app.app_context():
            db.drop_all()
            db.create_all()
            inspector = inspect(db.engine)
            self.table_names = inspector.get_table_names()

    @pytest.mark.parametrize('table_name', [
            'agreements',
            'permissions',
            'users',
    ])
    def test_tables_are_created_in_database(self, table_name):
        assert table_name in self.table_names

    def teardown_method(self):
        with app.app_context():
            db.drop_all()