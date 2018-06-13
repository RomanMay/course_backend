from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from app.models import User
from app.database import db_session, init_db

from app.views.main import main
from app.views.user import user
from app.views.admin import admin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['ADMINS'] = [
    'kirill',
    'romanmay',
    'roma'
]

app.register_blueprint(main)
app.register_blueprint(user)
app.register_blueprint(admin)
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
