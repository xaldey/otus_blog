from flask import Flask, render_template
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from webapp.models import Session, User
from webapp.views import auth_blueprint, blog_blueprint
from flask_moment import Moment


app = Flask(__name__)
app.config.from_pyfile('config.py')
bootstrap = Bootstrap(app)
moment = Moment(app)


app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(blog_blueprint, url_prefix="/")


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Session.query(User).filter_by(id=user_id).one_or_none()

#
# @app.route("/")
# def index():
#     return render_template("blog/index.html")


@app.teardown_request
def remove_session(*args):
    Session.remove()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)
