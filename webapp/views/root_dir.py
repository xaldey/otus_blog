from logging import getLogger
from flask import Blueprint, render_template
from flask_login import current_user, login_required
from datetime import datetime


from webapp.models import Session, User, Post, Tag
blog_blueprint = Blueprint("/", __name__)
logger = getLogger(__name__)


def show_all_posts_of_user(user):
    session = Session()
    query_posts = session.query(Post).filter(User.id == 2)
    for post in query_posts:
        return post.title, post.user
    session.close()


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
    session = Session()
    all_posts = session.query(Post).all()
    return render_template("blog/index.html", posts=all_posts, user=current_user, current_time=datetime.utcnow())


@blog_blueprint.route("/about/", endpoint="about")
def about():
    return render_template("blog/about.html")


@blog_blueprint.route("/post/<int:id>")
def post(id):
    session = Session()
    query_post = session.query(Post)
    post = query_post.filter_by(id=id).one()
    return render_template('blog/post.html', post=post)


@blog_blueprint.route("/login", endpoint="login")
def login():
    return render_template("auth/login.html")


@blog_blueprint.route("/protected/", endpoint="protected")
@login_required
def protected():
    return "!!!Это видно только залогиненным пользователям!!! Путь 'http://127.0.0.1:5000/protected/' "


# TODO Надо делать запросы в БД по аналогии с регистрацией/авторизацией и сверкой пользователей
# TODO Сделать выборку запроса и передавать в шаблон
