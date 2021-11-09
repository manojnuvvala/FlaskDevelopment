from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.validators import Required, Email, EqualTo
from wtforms import StringField, PasswordField, SubmitField

from .models import User


class RegistrationForm(FlaskForm):
    email = StringField("Your Email Address", validators=[Required(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            Required(),
            EqualTo("confirm_password", message="Passwords must match"),
        ],
    )
    confirm_password = PasswordField("Confirm Password", validators=[Required()])
    submit = SubmitField("Sign Up")

    def validate_email(self, data_field):
        if User.query.filter_by(email=data_field.data).first():
            raise ValidationError("There is already an account with this email")


class LoginForm(FlaskForm):
    email = StringField("Your Email Address", validators=[Required(), Email()])
    password = PasswordField("Password", validators=[Required()])
    submit = SubmitField("Sign In")


class JokeForm(FlaskForm):
    submit = SubmitField("Get Another Joke")
