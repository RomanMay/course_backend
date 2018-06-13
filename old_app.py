from app.forms import RegForm, LoginForm, OfferForm
from app.models import User, Offer, Order
from flask_cors import CORS
from app.database import db_session, init_db
from flask import Flask, request, render_template, redirect
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')
app.config.from_object('config')
CORS(app)







@app.route('/new_orders')
def new_orders():
    return render_template('new.html', orders=Order.query.filter_by(status="pending"))


@app.route('/rejected_orders')
def rejected():
    return render_template('rejected.html', orders=Order.query.filter_by(status="rejected"))


@app.route('/accepted_orders')
def accepted():
    return render_template('accepted.html')


@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        db_session.add(User(form.username.data, generate_password_hash(form.password.data), form.email.data, 'user'))
        db_session.commit()
        return redirect('/login')
    return render_template('registration.html', form=form)


@app.route('/check_user_by_id', methods=['GET'])
def check_user_by_id():
    username = request.args.get('username')
    return str(User.query.get(username))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    init_db()
    login_manager.init_app(app)
    app.run(host="0.0.0.0", debug=True)
