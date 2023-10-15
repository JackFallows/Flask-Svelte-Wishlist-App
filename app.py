# Python standard libraries
import os

if os.environ.get("WORKING_DIR") is not None:
    os.chdir(os.environ.get("WORKING_DIR"))

# Third party libraries
from flask import (
    Flask,
    send_from_directory
)
from flask_login import (
    LoginManager
)

# Internal imports
from helpers import custom_render_template

from data_access.db import init_db_command
from data_access.models.user import User

# Flask app setup
template_dir = os.path.dirname(__file__)
template_dir = os.path.join(template_dir, 'client', 'public')
app = Flask(__name__, template_folder=template_dir)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

from views.auth import auth
from views.external_auth import external_auth
from views.wishlist import wishlist
from views.profile import profile
from views.share import share

from api.users import users
from api.wishlists import wishlists
from api.wishlist_items import wishlist_items
from api.notifications import notifications

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(external_auth, url_prefix='/auth/external')
app.register_blueprint(wishlist, url_prefix='/wishlist')
app.register_blueprint(profile, url_prefix='/profile')
app.register_blueprint(share, url_prefix='/share')

app.register_blueprint(users, url_prefix='/api/users')
app.register_blueprint(wishlists, url_prefix='/api/wishlists')
app.register_blueprint(wishlist_items, url_prefix='/api/wishlist_items')
app.register_blueprint(notifications, url_prefix='/api/notifications')

# User session management setup
login_manager = LoginManager()
login_manager.login_view = 'index' # redirect to home page if user is not logged in when trying to access pages where login is required
login_manager.init_app(app)

# Database setup
with app.app_context():
    init_db_command()

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    return custom_render_template("index.html")

# Serve the content for the pages - JS, CSS, etc.
@app.route("/<path:path>")
def home(path):
    return send_from_directory("client/public", path)


if __name__ == "__main__":
    app.run(debug=True, ssl_context=('secure/cert.pem', 'secure/key.pem'))

