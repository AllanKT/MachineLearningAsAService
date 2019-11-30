
# -*- coding: utf-8 -*-


"""Script to get environments variables."""

import os
import datetime


def get_env_variable(name):
    """Pick up the contents of environment variables."""
    try:
        return os.environ[name]
    except KeyError:
        message = f"Expected environment variable '{name}' not set."
        raise Exception(message)


class Configuration(object):
    """Interacting with environment variables."""

    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(16)
    ASSETS_DEBUG = True
    ENV = 'development'
    RESTPLUS_VALIDATE = True

    # MAIL CONFIGURATIONS
    MAIL_FROM = get_env_variable('MAIL_FROM')
    MAIL_CC = get_env_variable("MAIL_CC")
    MAIL_USERNAME = get_env_variable('MAIL_USERNAME')
    MAIL_PASSWORD = get_env_variable('MAIL_PASSWORD')
    MAIL_SERVER = get_env_variable('MAIL_SERVER')
    MAIL_PORT = get_env_variable('MAIL_PORT')

    ACCESS_KEY = get_env_variable('ACCESS_KEY')
    SECRET_KEY = get_env_variable('SECRET_KEY')
    BUCKET_NAME = get_env_variable('BUCKET_NAME')
