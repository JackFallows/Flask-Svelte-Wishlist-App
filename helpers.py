from os import listdir
from os.path import isfile, join

from flask import render_template
from flask_login import current_user

from decorators.auth import ENABLE_INTERNAL_AUTH

bundle_files_path = 'client/public/build'

def custom_render_template(template_name, **context):
    # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    bundle_files = [f for f in listdir(bundle_files_path) if isfile(join(bundle_files_path, f))]
    auto_bundles = list(filter(lambda f: f.startswith('src_') or f.startswith('vendors-'), bundle_files))
    
    return render_template(
        template_name_or_list=template_name,
        user=current_user,
        internal_login_enabled= None if ENABLE_INTERNAL_AUTH is None or ENABLE_INTERNAL_AUTH.lower() == 'false' else 'true',
        auto_bundles=auto_bundles,
        **context
    )
