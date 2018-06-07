from forms import RegForm, LoginForm
from models import User, Offer, Order
from flask_cors import CORS
from database import db_session, init_db
from flask import Flask, request, render_template, redirect
from flask_login import LoginManager, UserMixin, login_required, current_user, logout_user, login_user

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')
login_manager = LoginManager()

app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
CORS(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        if user:
            user.authenticated = True
            db_session.add(user)
            db_session.commit()
            login_user(user, remember=True)
        return redirect('/')
    return render_template('log_in.html', form=form)


@app.route('/add_offer')
def add_offer():
    return render_template('add_form.html')


@app.route('/personal_room')
def personal_room():
    return render_template('pc1.html')


@app.route('/reg', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        db_session.add(User(form.username.data, form.password.data, form.email.data, 'user'))
        db_session.commit()
        return redirect('/')
    return render_template('log_in.html', form=form)


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
