from forms import RegForm, LoginForm, OfferForm
from models import User, Offer, Order
from flask_cors import CORS
from database import db_session, init_db
from flask import Flask, request, render_template, redirect
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')
app.config.from_object('config')
CORS(app)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.username not in app.config['ADMINS']:
            return 'You are not admin'
        else:
            return f(*args, **kwargs)

    return decorated


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.hash, form.password.data):
                login_user(user)
                return redirect('/personal_room')
    return render_template('login.html', form=form)


""" START USER SECTION """


@app.route('/personal_room')
@login_required
def personal_room():
    return render_template('pc1.html')


@app.route('/check_user', methods=['GET'])
@login_required
def check_user():
    return "Hello user: " + str(current_user.username) + " : " + str(current_user.email)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db_session.add(user)
    db_session.commit()
    logout_user()
    return redirect('/')


""" END USER SECTION """

""" START ADMIN SECTION """


@app.route('/delete_offer', methods=['POST'])
@login_required
@admin_required
def delete_offer():
    offer_name = request.form['offer_name']
    offer = Offer.query.filter_by(name=offer_name).first()
    if offer:
        db_session.delete(offer)
        db_session.commit()
        return 'ok'
    return 'Offer does not exist.'


@app.route('/add_offer', methods=['GET', 'POST'])
@login_required
@admin_required
def add_offer():
    form = OfferForm()
    if form.validate_on_submit():
        offer = Offer.query.filter_by(name=form.name.data).first()
        if not offer:
            db_session.add(Offer(form.name.data, form.cost.data, form.description.data, form.capacity.data))
            db_session.commit()
        return redirect('/all_offers')
    return render_template('add_offer.html', form=form)


@app.route('/all_offers')
@login_required
@admin_required
def all_offers():
    return render_template('all_offers.html', offers=Offer.query.all())


@app.route('/archive')
def archive():
    return render_template('archive.html', orders=Order.query.all())


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
