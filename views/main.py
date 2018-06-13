from forms import RegForm
from forms import LoginForm

from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template

from models import User
from database import db_session

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

main = Blueprint('main', __name__, template_folder='templates', static_folder='static', static_url_path='/static')


@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')


@main.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        db_session.add(User(form.username.data, generate_password_hash(form.password.data), form.email.data, 'user'))
        db_session.commit()
        return redirect('/login')
    return render_template('registration.html', form=form)
