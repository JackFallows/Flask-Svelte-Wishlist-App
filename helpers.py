from flask import render_template
from flask_login import current_user

from decorators import ENABLE_INTERNAL_AUTH

def custom_render_template(template_name, **context):
    return render_template(
        template_name_or_list=template_name,
        user=current_user,
        internal_login_enabled=ENABLE_INTERNAL_AUTH,
        **context
    )
