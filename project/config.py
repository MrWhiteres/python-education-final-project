"""
Module that contains a package of settings in the flask configuration.
"""
from os import environ

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    JSON_AS_ASCII = False
    TESTING = False
    url_db = f"postgresql://{environ['POSTGRES_USER']}:" \
             f"{environ['POSTGRES_PASSWORD']}@db:5432/{environ['POSTGRES_DB']}"
    SQLALCHEMY_DATABASE_URI = url_db
    SQLALCHEMY_TRACK_MODIFICATION = False
    SECRET_KEY = environ['SECRET_KEY']
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True


class TestConfig(BaseConfig):
    TESTING = True
