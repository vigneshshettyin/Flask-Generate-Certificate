import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))

with open('import.json', 'r') as c:
    env_var = json.load(c)["jsondata"]

DATABASE_URI = env_var["databaseUri"]
if DATABASE_URI.startswith("postgres://"):
    DATABASE_URI = DATABASE_URI.replace("postgres://", "postgresql://", 1)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'jdjsdjJJJJjhi*(%#@-CGV-PORTAL-VERIFY-@)(&$%wer387jjhdsujs28729&&*(*&'
    SQLALCHEMY_DATABASE_URI = DATABASE_URI


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
