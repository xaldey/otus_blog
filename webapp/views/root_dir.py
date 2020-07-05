from logging import getLogger
from werkzeug.exceptions import BadRequest, InternalServerError
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import current_user, login_required
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


from webapp.models import Session, User, Post, Tag
blog_blueprint = Blueprint("/", __name__)
logger = getLogger(__name__)


class NameForm(FlaskForm):
    name = StringField('Как к вам обращаться?', validators=[DataRequired()])
    submit = SubmitField('Отправить')


def show_posts_and_tags():
    session = Session()
    query_posts = session.query(Post)
    # query_tags = session.query(Tag)
    query_posts = query_posts.all()
    print("Вывести все посты и их теги:")
    for post in query_posts:
        print(post, post.tags)
        return post, post.tags
    session.close()


def show_posts_without_tags():
    session = Session()
    query_posts = session.query(Post)
    # query_tags = session.query(Tag)
    query_posts = query_posts.all()
    print("Вывести все посты без тегов:")
    return query_posts
    for post in query_posts:
        if post.tags:
            pass
        else:
            print(post)
            return post.title + ' ' + post.text
    session.close()


@blog_blueprint.route("/", methods=['GET', 'POST'], endpoint="index")
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Похоже, вы сменили имя?')
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    show_posts_without_tags()
    return render_template("blog/index.html", form=form, name=session.get('name'), user=current_user, post_wo_tags=show_posts_without_tags(),
                           posts_all=show_posts_and_tags(), current_time=datetime.utcnow())


@blog_blueprint.route("/add_post", endpoint="add_post")
def add_post():
    return render_template("add_post.html", user=current_user)


@blog_blueprint.route("/login", endpoint="login")
def login():
    return render_template("auth/login.html")


@blog_blueprint.route("/protected/", endpoint="protected")
@login_required
def protected():
    return "!!!Это видно только залогиненным пользователям!!!"


# TODO Надо делать запросы в БД по аналогии с регистрацией/авторизацией и сверкой пользователей
# TODO Сделать выборку запроса и передавать в шаблон
