import pytest
from werkzeug.exceptions import NotFound

from ..fixtures.app_fixtures import app
from application.extensions import db
from application.extensions import ma
from application.utils.crud import CommonCRUD


class SimpleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))


class SimpleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SimpleModel

    id = ma.auto_field()
    name = ma.auto_field()


class TestCommonCRUD:
    def setup_method(self):
        with app.app_context():
            db.create_all()

    def test_get_all(self):
        with app.app_context():
            response = CommonCRUD.get_all(SimpleSchema(), SimpleModel.query)
            assert response.status_code == 200

    def test_create(self):
        with app.app_context():
            data = {"id": 1, "name": "Test"}
            response = CommonCRUD.post(SimpleSchema(), SimpleModel, data)
            assert response[1] == 201
            assert response[0].json["name"] == "Test"
            assert response[0].json["id"] == 1

    def test_get_one(self):
        with app.app_context():
            # Creating entry
            data = {"id": 1, "name": "Test"}
            CommonCRUD.post(SimpleSchema(), SimpleModel, data)

            # Finding entry
            response = CommonCRUD.get_one(SimpleSchema(), SimpleModel.query.filter_by(id=1))
            assert response.json["name"] == "Test"
            assert response.json["id"] == 1

    def test_get_not_existing(self):
        with app.app_context():
            # Try to find not existing entry
            with pytest.raises(NotFound) as exception_info:
                CommonCRUD.get_one(SimpleSchema(), SimpleModel.query.filter_by(id=100))
            assert str(exception_info.value) == (
                "404 Not Found: The requested URL was not found on the server. "
                "If you entered the URL manually please check your spelling "
                "and try again."
            )

    def test_update_with_put_method(self):
        with app.app_context():
            # Creating an initial entry
            data = {"id": 1, "name": "Test"}
            CommonCRUD.post(SimpleSchema(), SimpleModel, data)

            # Updating the entry
            updated_data = {"name": "Updated"}
            response = CommonCRUD.put(SimpleSchema(), SimpleModel.query.filter_by(id=1), updated_data)
            assert response.status_code == 200
            assert response.json["name"] == "Updated"
            assert response.json["id"] == 1

    def test_put_not_existing(self):
        with app.app_context():
            # Try to find not existing entry
            with pytest.raises(NotFound) as exception_info:
                updated_data = {"name": "Updated"}
                CommonCRUD.put(SimpleSchema(), SimpleModel.query.filter_by(id=1), updated_data)
            assert str(exception_info.value) == (
                "404 Not Found: The requested URL was not found on the server. "
                "If you entered the URL manually please check your spelling "
                "and try again."
            )

    def test_update_with_patch_method(self):
        with app.app_context():
            # Creating an initial entry
            data = {"id": 1, "name": "Test"}
            CommonCRUD.post(SimpleSchema(), SimpleModel, data)

            # Updating the entry
            updated_data = {"name": "Updated"}
            response = CommonCRUD.patch(SimpleSchema(), SimpleModel.query.filter_by(id=1), updated_data)
            assert response.status_code == 200
            assert response.json["name"] == "Updated"
            assert response.json["id"] == 1

    def test_delete(self):
        with app.app_context():
            # Creating an initial entry
            data = {"id": 1, "name": "Test"}
            CommonCRUD.post(SimpleSchema(), SimpleModel, data)

            # Deleting the entry
            response = CommonCRUD.delete(SimpleModel.query.filter_by(id=1))
            assert response[1] == 204
            assert SimpleModel.query.filter_by(id=1).first() is None

    def test_delete_not_existing(self):
        with app.app_context():
            # Try to find not existing entry
            with pytest.raises(NotFound) as exception_info:
                CommonCRUD.delete(SimpleModel.query.filter_by(id=1))
            assert str(exception_info.value) == (
                "404 Not Found: The requested URL was not found on the server. "
                "If you entered the URL manually please check your spelling "
                "and try again."
            )

    def teardown_method(self):
        with app.app_context():
            db.drop_all()
