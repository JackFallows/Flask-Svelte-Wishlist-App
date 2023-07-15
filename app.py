# Python standard libraries
import os

# Third party libraries
from flask import (
    Flask,
    send_from_directory,
    render_template
)
from flask_login import (
    LoginManager,
    current_user
)

# Internal imports
from data_access.db import init_db_command
from data_access.models.user import User

# Flask app setup
template_dir = os.path.dirname(__file__)
template_dir = os.path.join(template_dir, 'client', 'public')
app = Flask(__name__, template_folder=template_dir)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

from views.auth import auth
from views.edit import edit

from api.wishlists import wishlists
from api.wishlist_items import wishlist_items

app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(edit, url_prefix='/edit')

app.register_blueprint(wishlists, url_prefix='/api/wishlists')
app.register_blueprint(wishlist_items, url_prefix='/api/wishlist_items')

# User session management setup
login_manager = LoginManager()
login_manager.login_view = 'index' # redirect to home page if user is not logged in when trying to access pages where login is required
login_manager.init_app(app)

# Database setup
init_db_command()

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    return render_template("index.html", user=current_user)

# Serve the content for the pages - JS, CSS, etc.
@app.route("/<path:path>")
def home(path):
    return send_from_directory("client/public", path)


if __name__ == "__main__":
    app.run(debug=True, ssl_context=('secure/cert.pem', 'secure/key.pem'))

