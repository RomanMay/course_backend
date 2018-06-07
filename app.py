from forms import RegForm
from models import User, Offer, Order
from flask_cors import CORS
from database import db_session, init_db
from flask import Flask, request, render_template, redirect

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')

app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegForm()
    data_valid = form.validate()
    print(data_valid)
    if data_valid:
        db_session.add(User(form.username.data, form.password.data, form.email.data, 'user'))
        db_session.commit()
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


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", debug=True)
