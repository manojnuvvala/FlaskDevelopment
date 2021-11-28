from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

import os
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE "] = 20
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 100
app.secret_key = 'secret string'
db = SQLAlchemy(app)
db.create_all()
csrf_protection = CSRFProtect()


def create_app():

    app = Flask(__name__)
    #app.config.from_pyfile("config.py")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_POOL_SIZE "] = 20
    app.config["SQLALCHEMY_MAX_OVERFLOW"] = 100
    app.secret_key = 'secret string'
    db = SQLAlchemy(app)
    from .views import app as main_blueprint

    db.init_app(app)
    csrf_protection.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app
