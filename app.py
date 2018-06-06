import json

import jwt
import datetime
from models import User, Offer, Order
from flask_cors import CORS
from database import db_session, init_db
from flask import Flask, request, jsonify, render_template
from functools import wraps

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')

app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('log_in.html')

@app.route('/add_offer')
def add_offer():
    return render_template('add_form.html')

@app.route('/personal_room')
def personal_room():
    return render_template('pc1.html')

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            token = request.form['token']
        if not token:
            return jsonify({'message': 'Token is missing!'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'})
        return f(*args, **kwargs)

    return decorated


@app.route('/is_login', methods=['GET'])
@login_required
def is_login():
    return 'ok'


@app.route('/reg', methods=['POST'])
def register():
    user = User(request.form['username'], request.form['password'], request.form['email'])
    db_session.add(user)
    db_session.commit()
    return 'ok'


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", debug=True)
