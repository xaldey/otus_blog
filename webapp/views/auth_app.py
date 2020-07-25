from logging import getLogger
from werkzeug.exceptions import BadRequest, InternalServerError
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required


from webapp.models import Session, User, Post
auth_blueprint = Blueprint("auth", __name__)
logger = getLogger(__name__)


@auth_blueprint.route("/", endpoint="index")
def index():
    session = Session()
    query_posts = session.query(Post).filter_by(user_id=current_user.id).all()

    return render_template("auth/index.html", user=current_user, posts=query_posts)


def validate_data(username, password):
    if not (
            username
            and len(username) >= 3
            and password
            and len(password) >= 8
    ):
        raise BadRequest("Username has to be at least 3 symbols and password minimum 8")


def validate_username_unique(username):
    if Session.query(User).filter_by(username=username).count():
        raise BadRequest(f"User with username {username!r} already  exists!")


def get_username_and_password():
    username = request.form.get("username")
    password = request.form.get("password")
    validate_data(username, password)

    return username, password


@auth_blueprint.route("/register/", methods=("GET", "POST"), endpoint="register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.index"))

    if request.method == "GET":
        return render_template("auth/register.html")

    username, password = get_username_and_password()
    validate_username_unique(username)

    user = User(username, password)
    Session.add(user)

    try:
        Session.commit()
    except Exception as e:
        logger.exception("Error creating user!!")
        Session.rollback()
        raise InternalServerError(f"Could not create user! Error: {e}")

    login_user(user)
    return redirect(url_for("auth.index"))


@auth_blueprint.route("/login/", methods=("GET", "POST"), endpoint="login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.index"))

    if request.method == "GET":
        return render_template("auth/login.html")

    username, password = get_username_and_password()
    user = Session.query(User).filter(
        User.username == username,
    ).one_or_none()

    if user.password != User.hash_password(password):
        return render_template("auth/login.html", error_text="Invalid username or password!")

    login_user(user)
    return redirect(url_for("auth.index"))


@auth_blueprint.route("/logout/", endpoint="logout")
def logout():
    logout_user()
    return redirect(url_for("/.about"))


@auth_blueprint.route('/add/', endpoint="add")
@login_required
def add():
    return render_template("auth/add.html")


@auth_blueprint.route("/addpost", methods=['POST'])
@login_required
def addpost():
    title = request.form['title']
    user = current_user
    content = request.form['content']

    post = Post(title=title, user=user, text=content)

    Session.add(post)
    Session.commit()

    return redirect(url_for('/.index'))
