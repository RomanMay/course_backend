from app.forms import RegForm
from app.forms import LoginForm

from flask import redirect
from flask import Blueprint
from flask import render_template

from app.models import User
from app.database import db_session

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from flask_login import login_user

main = Blueprint('main', __name__, template_folder='templates', static_folder='static', static_url_path='/static')


@main.route('/')
@main.route('/index')
def index():
    return render_template('main/index.html')


@main.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        db_session.add(User(form.username.data, generate_password_hash(form.password.data), form.email.data, 'user'))
        db_session.commit()
        return redirect('/login')
    return render_template('main/registration.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.hash, form.password.data):
                login_user(user)
                return redirect('/personal_room')
    return render_template('main/login.html', form=form)