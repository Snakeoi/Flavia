from application import create_app
from application.extensions import db

app = create_app("testing")

class DatabaseCreateDropFixture:

    def setup_method(self):
        with app.app_context():
            db.drop_all()
            db.create_all()

    def teardown_method(self):
        with app.app_context():
            db.drop_all()