from flask import Blueprint

from helpers import custom_render_template

share = Blueprint('share', __name__)

@share.route('/<share_guid>')
def wishlist(share_guid):
    return custom_render_template("share.html")
