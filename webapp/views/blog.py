from logging import getLogger
from werkzeug.exceptions import BadRequest, InternalServerError
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required


from webapp.models import Session, User

blog_blueprint = Blueprint("/", __name__)

logger = getLogger(__name__)


@blog_blueprint.route("/", endpoint="index")
def index():
    return render_template("index.html", user=current_user)


@blog_blueprint.route("/protected/", endpoint="protected")
@login_required
def protected():
    return "!!!Это видно только залогиненным пользователям!!!"
