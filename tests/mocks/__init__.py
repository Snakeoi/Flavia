from flask_login import UserMixin


class MockUser(UserMixin):
    def __init__(self, permissions):
        self.id = 9999999 # This is a mock user, so we don't need to set a real ID for our
        self.email = "john.doe@example.com"
        self.username = "John Doe"
        self.confirmed = True
        self.permissions = permissions

    def have_permission(self, *permissions):
        return all(permission in self.permissions for permission in permissions)