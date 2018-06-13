from flask import redirect
from flask import Blueprint
from flask import render_template

from app.models import User
from app.database import db_session

from flask_login import login_required, current_user, logout_user

user = Blueprint('user', __name__, template_folder='templates', static_folder='static', static_url_path='/static')


@user.route('/personal_room')
@login_required
def personal_room():
    return render_template('user/personal_room.html')


@user.route('/add_order', methods=['POST'])
@login_required
def add_order():
    pass


@user.route('/check_user', methods=['GET'])
@login_required
def check_user():
    return "Hello user: " + str(current_user.username) + " : " + str(current_user.email)


@user.route('/logout', methods=['GET'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db_session.add(user)
    db_session.commit()
    logout_user()
    return redirect('/')