import random
from datetime import datetime, timedelta

from sqlalchemy import UniqueConstraint
from flask_jwt_extended import create_access_token
from flask_jwt_extended import decode_token
from flask_login import UserMixin
from jwt import ExpiredSignatureError
from werkzeug.security import generate_password_hash, check_password_hash

from application.extensions import db, login_manager


class PermissionCodes:
    MANAGER = 'manager'
    ADMIN = 'admin'

    LISTED = [
        ADMIN,
        MANAGER,
    ]


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    codename = db.Column(db.String(16), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'codename', name='_user_codename_uc'),)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    password_hash = db.Column(db.Text)
    reset_token = db.Column(db.Text)
    confirmed = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    permissions = db.relationship(
        'Permission',
        backref='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def permissions_list(self) -> list[str]:
        return [permission.codename for permission in self.permissions]

    def have_permission(self, *args):
        if len(args) == 0:
            return True

        permissions = self.permissions_list
        for arg in args:
            if arg in permissions:
                return True
        return False

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        additional_claims = {"confirm": True}
        expires = timedelta(seconds=expiration)
        return create_access_token(
            identity=self.email,
            additional_claims=additional_claims,
            expires_delta=expires
        )

    def confirm(self, token):
        try:
            decoded_token = decode_token(token)
            if decoded_token.get('confirm'):
                self.confirmed = True
                return True
            else:
                return False
        except ExpiredSignatureError:
            return False

    def generate_pin(self) -> str:
        return ''.join([str(random.randint(0, 9)) for i in range(6)])

    def set_reset_password_pin(self, expiration=3600):
        pin = self.generate_pin()
        additional_claims = {
            "pin": pin
        }
        expires = timedelta(seconds=expiration)
        token = create_access_token(
            identity=self.email,
            additional_claims=additional_claims,
            expires_delta=expires
        )
        self.reset_token = token
        db.session.commit()
        return pin

    def reset_password(self, pin, new_password):
        if not self.reset_token:
            return False
        try:
            decoded_token = decode_token(self.reset_token)
            if str(decoded_token['pin']) == str(pin):
                self.password = new_password
                self.reset_token = None
                db.session.commit()
                return True
            else:
                return False
        except ExpiredSignatureError:
            return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

class Agreement(db.Model):
    __tablename__ = 'agreements'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)