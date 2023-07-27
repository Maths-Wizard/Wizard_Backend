import os
from flask import Flask
from wizard.configs.config import Config
from wizard.configs.dbase import db, init_app
# from models.user import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    db.app = app
    init_app(app)

    return app
