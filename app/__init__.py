from flask import Flask

from app.models import User
from app.views.main import main
from app.views.user import user
from flask_cors import CORS
from app.database import db_session, init_db
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['ADMINS'] = [
    'kirill',
    'romanmay'
]

app.register_blueprint(main)
app.register_blueprint(user)
CORS(app)

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def create_app():
    init_db()
    login_manager.init_app(app)
    return app
