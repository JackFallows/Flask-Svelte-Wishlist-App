# Python standard libraries
import os
import sqlite3

# Third party libraries
from flask import (
    Flask,
    send_from_directory,
    render_template
)
from flask_login import (
    LoginManager,
    current_user,
)

# Internal imports
from data_access.db import init_db_command
from data_access.models.user import User

# Flask app setup
template_dir = os.path.dirname(__file__)
template_dir = os.path.join(template_dir, 'client', 'public')
app = Flask(__name__, template_folder=template_dir)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

from auth import auth

app.register_blueprint(auth, url_prefix='/')

# User session management setup
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html", user=current_user)

    return '<a class="button" href="/login">Google Login</a>'

# Serve the content for the pages - JS, CSS, etc.
@app.route("/<path:path>")
def home(path):
    return send_from_directory("client/public", path)


if __name__ == "__main__":
    app.run(debug=True, ssl_context=('secure/cert.pem', 'secure/key.pem'))

