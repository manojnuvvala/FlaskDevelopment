from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy


login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"

db = SQLAlchemy()
csrf_protection = CSRFProtect()


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    from .views import app as main_blueprint

    db.init_app(app)
    csrf_protection.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app
