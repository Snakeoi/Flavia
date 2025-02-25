from flask_login import login_user

from application.models import User
from tests.fixtures.make_user import make_user
from ...fixtures.app_fixtures import app
from application.extensions import db

class TestCommonCRUD:
    def setup_method(self):
        with app.app_context():
            db.drop_all()
            db.create_all()

    def test_get_all_users_returns_list_of_users(self):
        with app.test_request_context():
            with app.test_client() as client:
                admin = make_user(permissions=['admin'])
                login_user(admin)
                response = client.get("/api/user/")
                assert response.status_code == 200
                assert isinstance(response.json, list)

    def test_get_all_users_is_impassible_if_logged_user_is_not_admin(self):
        with app.test_request_context():
            with app.test_client() as client:
                not_admin = make_user(permissions=[])
                login_user(not_admin)
                response = client.get("/api/user/")
                assert response.status_code == 403

    def test_post_create_new_user_and_sends_confirmation_email(self):
        with app.test_request_context():
            with app.test_client() as client:
                admin = make_user(permissions=['admin'])
                login_user(admin)
                response = client.post("/api/user/", json={
                    "email": "kate.doe@example.com",
                    "username": "Kate Doe",
                    "password": "P@ssw0rd",
                    "permissions": [],
                    "send_confirmation_email": False
                })
                user = User.query.filter_by(email="kate.doe@example.com").first()
                assert user is not None
                assert response.status_code == 201

    def test_post_create_new_user_is_impassible_if_logged_user_is_not_admin(self):
        with app.test_request_context():
            with app.test_client() as client:
                not_admin = make_user(permissions=[])
                login_user(not_admin)
                response = client.post("/api/user/", json={
                    "email": "kate.doe@example.com",
                    "username": "Kate Doe",
                    "password": "P@ssw0rd",
                    "permissions": [],
                    "send_confirmation_email": False
                })
                user = User.query.filter_by(email="kate.doe@example.com").first()
                assert user is None
                assert response.status_code == 403

    def test_post_create_new_user_is_impassible_with_existing_email_returns_error(self):
        with app.test_request_context():
            with app.test_client() as client:
                admin = make_user(email='john.doe@example.com', permissions=['admin'])
                login_user(admin)
                response = client.post("/api/user/", json={
                    "email": "john.doe@example.com",
                    "username": "John Doe",
                    "password": "P@ssw0rd",
                    "permissions": [],
                    "send_confirmation_email": False
                })
                users = User.query.filter_by(email="john.doe@example.com").all()
                assert len(users) == 1
                assert response.status_code == 400

    def test_user_view_get_returns_404_when_user_doesnt_exist(self):
        with app.test_request_context():
            with app.test_client() as client:
                admin = make_user(permissions=['admin'])
                login_user(admin)
                response = client.get("/api/user/100")
                assert response.status_code == 404

    def test_user_view_get_is_impassible_if_logged_user_is_not_admin(self):
        with app.test_request_context():
            with app.test_client() as client:
                not_admin = make_user(permissions=[])
                login_user(not_admin)
                response = client.get("/api/user/100")
                assert response.status_code == 403

    def test_user_view_get_returns_user(self):
        with app.test_request_context():
            with app.test_client() as client:
                admin = make_user(permissions=['admin'])
                login_user(admin)
                user = make_user(
                    email="kate.doe@example.com",
                    username="Kate Doe",
                    permissions=[]
                )
                response = client.get(f"/api/user/{user.id}")
                assert response.status_code == 200

    def test_patch_user_updates_user(self):
        with app.test_request_context():
            with app.test_client() as client:
                admin = make_user(permissions=['admin'])
                login_user(admin)
                user = make_user(
                    email="kate.doe@example.com",
                    username="Kate Doe",
                    permissions=[]
                )
                response = client.patch(f"/api/user/{user.id}", json={
                    "email": "maria.doe@example.com",
                    "username": "Maria Doe",
                    "permissions": ['admin'],
                })
                assert response.json['email'] == 'maria.doe@example.com'
                assert response.json['username'] == 'Maria Doe'
                assert response.json['permissions'] == ['admin']
                assert response.status_code == 200

    def test_patch_user_is_impassible_if_logged_user_is_not_admin(self):
        with app.test_request_context():
            with app.test_client() as client:
                not_admin = make_user(permissions=[])
                login_user(not_admin)
                user = make_user(
                    email="kate.doe@example.com",
                    username="Kate Doe",
                    permissions=[]
                )
                response = client.patch(f"/api/user/{user.id}", json={
                    "email": "maria.doe@example.com",
                    "username": "Maria Doe",
                    "permissions": ['admin'],
                })
                assert response.status_code == 403

    def test_patch_user_with_removing_admin_permission_on_logged_user_is_impassible(self):
        with app.test_request_context():
            with app.test_client() as client:
                admin = make_user(permissions=['admin'])
                login_user(admin)
                response = client.patch(f"/api/user/{admin.id}", json={
                    "email": "maria.doe@example.com",
                    "username": "Maria Doe",
                    "permissions": [],
                })
                user = User.query.filter_by(id=admin.id).first()
                assert response.status_code == 400
                assert response.json['errors'] == ['You cannot remove admin permission from yourself.']
                assert 'admin' in user.permissions_list
                assert user.username == 'John Doe'
                assert user.email == 'john.doe@example.com'

    def test_patch_user_with_editing_on_logged_user(self):
        with app.test_request_context():
            with app.test_client() as client:
                admin = make_user(permissions=['admin'])
                login_user(admin)
                response = client.patch(f"/api/user/{admin.id}", json={
                    "email": "maria.doe@example.com",
                    "username": "Maria Doe",
                    "permissions": ['admin'],
                })
                user = User.query.filter_by(id=admin.id).first()
                assert response.status_code == 200
                assert 'admin' in user.permissions_list
                assert user.username == 'Maria Doe'
                assert user.email == 'maria.doe@example.com'

    def test_delete_user_is_impassible_if_logged_user_is_not_admin(self):
        with app.test_request_context():
            with app.test_client() as client:
                not_admin = make_user(permissions=[])
                login_user(not_admin)
                user = make_user(
                    email="kate.doe@example.com",
                    username="Kate Doe",
                    permissions=[]
                )
                response = client.delete(f"/api/user/{user.id}")
                user = User.query.filter_by(id=user.id).first()
                assert response.status_code == 403
                assert user is not None

    def test_delete_user_is_impassible_if_logged_user_is_deleting_himself(self):
        with app.test_request_context():
            with app.test_client() as client:
                admin = make_user(permissions=['admin'])
                login_user(admin)
                response = client.delete(f"/api/user/{admin.id}")
                user = User.query.filter_by(id=admin.id).first()
                assert response.status_code == 400
                assert response.json['errors'] == ['You cannot delete yourself.']
                assert user is not None

    def test_delete_user_deletes_user(self):
        with app.test_request_context():
            with app.test_client() as client:
                admin = make_user(permissions=['admin'])
                login_user(admin)
                user = make_user(
                    email="kate.doe@example.com",
                    username="Kate Doe",
                    permissions=[]
                )
                response = client.delete(f"/api/user/{user.id}")
                user = User.query.filter_by(id=user.id).first()
                assert response.status_code == 204
                assert user is None