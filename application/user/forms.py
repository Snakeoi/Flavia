from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from . import validators_config


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(
            message=validators_config.Email.required.prompt
        ),
        Email(
            message=validators_config.Email.email.prompt
        )
    ])
    password = PasswordField('Password', validators=[
        DataRequired(
            message=validators_config.Password.required.prompt
        )
    ])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class _EmailAndPasswordForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(
            message=validators_config.Email.required.prompt
        ),
        Length(
            validators_config.Email.length.min,
            validators_config.Email.length.max,
            validators_config.Email.length.prompt,
        ),
        Email(
            message=validators_config.Email.email.prompt
        )
    ])
    password = PasswordField('Password', validators=[
        DataRequired(
            message=validators_config.Password.required.prompt
        ),
        Regexp(
            regex=validators_config.Password.regex.pattern,
            message=validators_config.Password.regex.prompt
        ),
        Length(
            min=validators_config.Password.length.min,
            max=validators_config.Password.length.max,
            message=validators_config.Password.length.prompt
        ),
    ])
    password2 = PasswordField('Confirm password', validators=[
        DataRequired(
            message=validators_config.PasswordRepeat.required.prompt
        ),
        EqualTo(
            'password',
            message=validators_config.PasswordRepeat.equal_to.prompt
        )
    ])


class RegistrationForm(_EmailAndPasswordForm):
    username = StringField('Username', validators=[
        DataRequired(
            message=validators_config.Username.required.prompt
        ),
        Length(
            min=validators_config.Username.length.min,
            max=validators_config.Username.length.max,
            message=validators_config.Username.length.prompt
        ),
        Regexp(
            regex=validators_config.Username.regex.pattern,
            message=validators_config.Username.regex.prompt
        )
    ])
    submit = SubmitField('Register')


class PasswordResetForm(_EmailAndPasswordForm):
    pin = IntegerField('PIN')
    submit = SubmitField('Reset Password')
