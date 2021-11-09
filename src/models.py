import random

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from src.app import db, login_manager


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password_hash = generate_password_hash(password)

    @property
    def password(self):
        raise AttributeError("Password cannot be read")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<User %r>" % self.email


class Joke(db.Model):

    __tablename__ = "jokes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    joke = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, joke, user_id=1):
        self.joke = joke
        self.user_id = user_id

    def save_joke(self):
        db.session.add(self)
        db.session.commit()

    def get_random_joke():
        return random.choice(Joke.query.all())

    def __repr__(self):
        return f"<Joke {self.id}, {self.joke}, {self.user_id}>"


@login_manager.user_loader
def load_user(user_id):
    from .models import User

    return User.query.get(user_id)
