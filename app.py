import json

import jwt
import datetime
from models import User, Offer, Order
from flask_cors import CORS
from database import db_session, init_db
from flask import Flask, request, jsonify, render_template
from functools import wraps

app = Flask(__name__, static_folder="static", template_folder="templates", static_url_path="/static")

app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
CORS(app)


@app.route('/')
def index():
    print(app.static_url_path)
    return render_template("index.html")


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


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if not registered_user:
        return 'Error login'
    token = jwt.encode(
        {
            'id': registered_user.id,
            'email': registered_user.email,
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=3600)
        },
        app.config['SECRET_KEY'])
    return jsonify(
        {
            'token': token.decode('UTF-8'),
            'id': registered_user.id,
            'email': registered_user.email
        })


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
