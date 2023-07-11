# Python standard libraries
import json
import os
import sqlite3

# Third party libraries
from flask import (
    Flask,
    send_from_directory,
    redirect,
    request,
    url_for,
    render_template
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from data_access.db import init_db_command
from data_access.models.user import User

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup

template_dir = os.path.dirname(__file__)
template_dir = os.path.join(template_dir, 'client', 'public')
app = Flask(__name__, template_folder=template_dir)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    # TODO fix
    #init_db_command()
    pass
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

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

@app.route("/login")
def login():
    # Find out what URL to hit for Google's login
    google_provider_cfg = get_google_provider_cfg()
    authorisation_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorisation_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to us
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow us to ask for 
    # things on behalf of user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    )

    # Parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens, let's find and hit the URL
    # from Google that gives us the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorised our
    # app, and now we've verified their email through Google
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    
    # Create a user in the db with the information provided by Google
    user = User(
        id_ = unique_id,
        name = users_name,
        email=users_email,
        profile_pic=picture
    )

    # Add to the db if it doesn't exist
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

def get_google_provider_cfg():
    # TODO add error handling
    return requests.get(GOOGLE_DISCOVERY_URL).json()

if __name__ == "__main__":
    app.run(debug=True, ssl_context=('secure/cert.pem', 'secure/key.pem'))

