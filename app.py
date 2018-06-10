from forms import RegForm, LoginForm, OfferForm
from models import User, Offer, Order
from flask_cors import CORS
from database import db_session, init_db
from flask import Flask, request, render_template, redirect
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from functools import wraps

login_manager = LoginManager()
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')
app.config.from_object('config')
CORS(app)


def admin_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
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

@app.route('/user_abonements')
def user_abonements():
    return render_template('user_abonements.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            login_user(user)
            return redirect('/personal_room')
    return render_template('login.html', form=form)


@app.route('/add_offer', methods=['GET', 'POST'])
@login_required
@admin_required
def add_offer():
    form = OfferForm()
    if form.validate_on_submit():
        offer = Offer.query.filter_by(name=form.name.data).first()
        if not offer:
            db_session.add(Offer(form.name.data, form.cost.data, form.description.data, form.capacity.data ))
            db_session.commit()
        return redirect('/all_abonements')
    return render_template('add_offer.html', form=form)

@app.route('/all_abonements')
def all_abonements():
    return render_template('all_abonements.html', offers=Offer.query.all())

@app.route('/archive')
def archive():
    return render_template('archive.html')

@app.route('/new_abonements')
def new_abonements():
    return render_template('new.html')

@app.route('/rejected')
def rejected():
    return render_template('rejected.html')

@app.route('/accepted')
def accepted():
    return render_template('accepted.html')

@app.route('/personal_room')
@login_required
def personal_room():
    return render_template('pc1.html')


@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        db_session.add(User(form.username.data, form.password.data, form.email.data, 'user'))
        db_session.commit()
        return redirect('/')
    return render_template('registration.html', form=form)


@app.route('/check_user', methods=['GET'])
@login_required
def check_user():
    return "Hello user: " + str(current_user.username) + " : " + str(current_user.email)


@app.route('/check_user_by_id', methods=['GET'])
def check_user_by_id():
    username = request.args.get('username')
    return str(User.query.get(username))


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db_session.add(user)
    db_session.commit()
    logout_user()
    return redirect('/')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    init_db()
    login_manager.init_app(app)
    app.run(host="0.0.0.0", debug=True)
