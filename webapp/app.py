from flask import Flask, render_template
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from webapp.models import Session, User
from webapp.views import auth_blueprint, blog_blueprint

app = Flask(__name__)
app.config.from_pyfile('config.py')
bootstrap = Bootstrap(app)


app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(blog_blueprint, url_prefix="/")


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Session.query(User).filter_by(id=user_id).one_or_none()


@app.route("/")
def index():
    return render_template("index.html")


@app.teardown_request
def remove_session(*args):
    Session.remove()


if __name__ == "__main__":
    app.run(debug=True)
