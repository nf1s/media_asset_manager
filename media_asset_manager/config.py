# -*- coding: utf-8 -*-
"""Configuration Module

Module handles the configuration of different environments (Dev, Test and Prod)
"""
import os

import dj_database_url
from dotenv import load_dotenv

# from corsheaders.defaults import default_headers


class Base:
    DEBUG = True
    HEROKU = os.getenv("HEROKU")
    DOCKER = os.getenv("DOCKER")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(BASE_DIR, ".env"))

    SECRET_KEY = os.environ["SECRET_KEY"]

    ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".ngrok.io"]

    MESSAGE_BROKER = os.environ["MESSAGE_BROKER"]

    CORS_ORIGIN_ALLOW_ALL = False
    CORS_ORIGIN_WHITELIST = ["http://localhost:3000"]


class Dev(Base):
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ORIGIN_WHITELIST = ["http://localhost:3000"]

    if Base.DOCKER:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "postgres",
                "USER": "postgres",
                "HOST": "db",
                "PORT": 5432,  # default postgres port
            }
        }
    else:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(Base.BASE_DIR, "db.sqlite3"),
            }
        }


class Test(Base):
    DEBUG = False

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "circleci_test",
            "USER": "circleci",
            "HOST": "localhost",
            "PORT": 5432,
        }
    }


class Staging(Base):
    DEBUG = False
    DATABASES = {}
    DATABASES["default"] = dj_database_url.config(conn_max_age=600)
    ALLOWED_HOSTS = ["ADD STAGING HOST"]
    CORS_ORIGIN_WHITELIST = ["ADD STAGING WHITELIST IF ANY"]


class Prod(Base):
    DEBUG = False
    DATABASES = {}
    DATABASES["default"] = dj_database_url.config(conn_max_age=600)
    ALLOWED_HOSTS = ["ADD PROD HOST"]
    CORS_ORIGIN_WHITELIST = ["ADD PROD WHITELIST IF ANY"]


def get_config():
    env = os.environ["ENV"]

    if env == "PROD":
        return Prod()

    if env == "TEST":
        return Test()

    if env == "STAGING":
        return Staging()

    return Dev()
