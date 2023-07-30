from flask import Flask
from wizard.configs.config import Config
from wizard.configs.dbase import db, init_app
from wizard.routes.auth import auth_bp
from wizard.routes.home import home_bp
from wizard.routes.user import user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    db.app = app
    init_app(app)

    return app


app = create_app()
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(user_bp)
