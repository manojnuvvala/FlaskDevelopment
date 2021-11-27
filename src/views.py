from flask import (
    abort,
    flash,
    url_for,
    request,
    redirect,
    Blueprint,
    session,
    render_template,
)
from flask_login import login_required, login_user, logout_user, current_user
from src.app import db
from .models import User, Joke
from .forms import JokeForm, JokeFormdata, RegistrationForm, LoginForm
from .utils import is_safe_url


app = Blueprint("auth", __name__)


@app.route("/", methods=["GET"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    return render_template("auth/home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        user.save_user()
        flash("User registered successfully")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            result = login_user(user)
            print(result)

            next = request.args.get("next")

            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for("auth.dashboard"))

        flash("Invalid email or Password")

    return render_template("auth/login.html", form=form)


@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
    form = JokeForm()
    if form.validate_on_submit():
        if form.submit.data:
            joke = Joke.get_random_joke().joke

            return render_template("jokes/dashboard.html", form=form, joke=joke)
        if form.another.data:
            form=JokeFormdata()
            return render_template("jokes/addjoke.html",form=form)
    return render_template("jokes/dashboard.html", form=form)

@app.route("/submited", methods=["POST", "GET"])
@login_required
def jokesubmited():
    form = JokeFormdata()
    if form.validate_on_submit():
        #user_id = session["user_id"]
        #print(user_id)
        print(current_user.id)
        formdata = Joke(joke=form.jokestring.data, user_id = current_user.id)
        db.session.add(formdata)
        db.session.commit()
        #formdata.save_joke()
        flash("Joke registered successfully")

        return redirect(url_for("auth.home"))

@app.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(url_for("auth.home"))

