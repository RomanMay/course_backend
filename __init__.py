from flask import Flask
from views.main import main
from flask_cors import CORS
from database import db_session, init_db

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(main)
CORS(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    init_db()

    app.run(host="0.0.0.0", debug=True)
