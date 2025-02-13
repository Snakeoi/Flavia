from marshmallow import validate

from application.extensions import ma

from application.models import User, Permission
from .. import validators_config


class PermissionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Permission

    codename = ma.auto_field()


class UserReadSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    confirmed = ma.auto_field()
    member_since = ma.auto_field()
    last_seen = ma.auto_field()
    permissions = ma.Pluck("PermissionSchema", "codename", many=True)


class UserCreateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field(
        required=True,
        validate=[
            validate.Length(
                min=validators_config.Username.length.min,
                max=validators_config.Username.length.max,
                error=validators_config.Username.length.prompt,
            ),
            validate.Regexp(
                regex=validators_config.Username.regex.pattern, error=validators_config.Username.regex.prompt
            ),
        ],
    )
    email = ma.auto_field(
        required=True,
        validate=[
            validate.Email(error=validators_config.Email.email.prompt),
            validate.Length(max=validators_config.Email.length.max, error=validators_config.Email.length.prompt),
        ],
    )
    permissions = ma.Pluck("PermissionSchema", "codename", many=True, required=True)
    password = ma.Str(
        required=True,
        validate=[
            validate.Regexp(
                regex=validators_config.Password.regex.pattern, error=validators_config.Password.regex.prompt
            ),
            validate.Length(
                min=validators_config.Password.length.min,
                max=validators_config.Password.length.max,
                error=validators_config.Password.length.prompt,
            ),
        ],
    )
    send_confirmation_email = ma.Bool(required=True)


class UserUpdateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field(
        validate=[
            validate.Length(
                min=validators_config.Username.length.min,
                max=validators_config.Username.length.max,
                error=validators_config.Username.length.prompt,
            ),
            validate.Regexp(
                regex=validators_config.Username.regex.pattern, error=validators_config.Username.regex.prompt
            ),
        ]
    )
    email = ma.auto_field(
        validate=[
            validate.Email(error=validators_config.Email.email.prompt),
            validate.Length(max=validators_config.Email.length.max, error=validators_config.Email.length.prompt),
        ]
    )
    permissions = ma.Pluck(
        "PermissionSchema",
        "codename",
        many=True,
    )
    password = ma.Str(
        validate=[
            validate.Regexp(
                regex=validators_config.Password.regex.pattern, error=validators_config.Password.regex.prompt
            ),
            validate.Length(
                min=validators_config.Password.length.min,
                max=validators_config.Password.length.max,
                error=validators_config.Password.length.prompt,
            ),
        ]
    )


class EmailSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    email = ma.auto_field(
        required=True,
        validate=[
            validate.Email(error=validators_config.Email.email.prompt),
            validate.Length(max=validators_config.Email.length.max, error=validators_config.Email.length.prompt),
        ],
    )
