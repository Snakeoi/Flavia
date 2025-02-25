from application.models import User, PermissionCodes, Permission
from application.extensions import db

def add_permissions(user: "User", permission_codes: list[str]):
    for permission in permission_codes:
        if permission in PermissionCodes.LISTED and permission not in user.permissions_list:
            db.session.add(
                Permission(
                    user_id=user.id,
                    codename=permission,
                )
            )

def make_user(email="john.doe@example.com", username="John Doe", password="P@ssw0rd", permissions=[]):

    user: "User" = User(email=email.lower(), username=username, password=password)
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(email=email).first()
    add_permissions(user, permissions)
    db.session.commit()
    return User.query.filter_by(email=email).first()