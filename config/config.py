"""
this file holds the application's config settings
    - DevelopementConfig Class holds configs for dev enrironment
    - TestingConfig holds config for testing environment
"""

import os
from dotenv import load_dotenv
from datetime import timedelta
# load env variables
load_dotenv('.env')
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    '''
        Base config class. Holds default config seetings for the app
    '''

    # define default configs
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASK_DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY', default='')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIMEZONE = 'Africa/Nairobi'
    JSONIFY_PRETTYPRINT_REGULAR = True
    SWAGGER = {
        'title': 'CEMA-HIS APIs',
        'uiversion': 3
    }
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)


class DevelopmentConfig(Config):
    '''
        config class to define developement environment configuration for the app
    '''
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    DEVELOPMENT = True
    FLASK_DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
            'DB_URL_DEV',
            default='sqlite:///' + os.path.join(
                basedir,
                'cema-his-dev.sqlite'
            )
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
            'DB_URL_TEST',
            default='sqlite:///' + os.path.join(
                basedir,
                'cema-his-test.sqlite'
            )
    )


config = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'default': DevelopmentConfig
}
