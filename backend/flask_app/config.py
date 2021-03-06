# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module has configurations for flask app."""

import logging
import os
from datetime import timedelta
CONFIG = {
    "development": "flask_app.config.DevelopmentConfig",
    "testing": "flask_app.config.TestingConfig",
    "production": "flask_app.config.ProductionConfig",
    "default": "flask_app.config.ProductionConfig"
}


class BaseConfig(object):
    """Base class for default set of configs."""

    DEBUG = False
    TESTING = False
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_TRACKABLE = True
    LOGGING_FORMAT = "[%(asctime)s] [%(funcName)-30s] +\
                                    [%(levelname)-6s] %(message)s"
    LOGGING_LOCATION = 'web.log'
    LOGGING_LEVEL = logging.DEBUG
    SECURITY_TOKEN_MAX_AGE = 600 * 300
    SECURITY_CONFIRMABLE = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'simple'
    SECURITY_PASSWORD_SALT = 'fsdpa98-0daso3da-09asdkasd-09SD0a'
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml',
                          'application/json', 'application/javascript']

    WTF_CSRF_ENABLED = False
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500

    # Change it based on your admin user, should ideally read from DB.
    ADMIN_EMAIL = 'zdeneksmejkal@gmail.com'
    ADMIN_PASSWORD = 'K9B6GaSS5'
    JWT_EXPIRES = timedelta(days=60)


class DevelopmentConfig(BaseConfig):
    """Default set of configurations for development mode."""

    DEBUG = True
    TESTING = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://kokot@localhost:3307/dojebhotov'
    SECRET_KEY = 'asdf98-0gvek0--adsols-0d20dokas'
    JWT_SECRET_KEY = 'another_super_awesome_secret_stuff_yo.'


class ProductionConfig(BaseConfig):
    """Default set of configurations for prod mode."""

    DEBUG = False
    TESTING = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SECRET_KEY = 'asdf98-0gvek0--adsols-0d20dokas'
    JWT_SECRET_KEY = 'another_super_awesome_secret_stuff_yo.'


class TestingConfig(BaseConfig):
    """Default set of configurations for test mode."""

    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'asdf98-0gvek0--adsols-0d20dokas'
    JWT_SECRET_KEY = 'another_super_awesome_secret_stuff_yo.'
