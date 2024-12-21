import os
import datetime


class Config:
    APP_NAME = 'FlaviaApp'
    MODE = os.environ.get('MODE', 'production')

    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY', '')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=5)

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', '')
    MAIL_PORT = os.environ.get('MAIL_PORT', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)

    EVERYONE_CAN_REGISTER = os.environ.get('EVERYONE_CAN_REGISTER', True)

    DB_NAME = os.environ.get('DB_NAME', 'flavia')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_NAME


class ConfigDev(Config):
    FLASK_DEBUG = True
    TESTING = False


class ConfigTesting(Config):
    FLASK_DEBUG = False
    TESTING = True


class ConfigProduction(Config):
    FLASK_DEBUG = False
    TESTING = False


assignment = {
    "development": ConfigDev,
    "testing": ConfigTesting,
    "production": ConfigProduction,
}
