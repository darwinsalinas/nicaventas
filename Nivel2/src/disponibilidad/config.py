import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Config(object):
    DEBUG = False
    TESTING = False

    DB_NAME = os.environ['POSTGRES_DB']
    DB_USER = os.environ['POSTGRES_USER']
    DB_PASS = os.environ['POSTGRES_PASSWORD']
    DB_SERVICE = os.environ['DB_SERVICE']
    DB_PORT = os.environ['DB_PORT']
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
    )

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app
