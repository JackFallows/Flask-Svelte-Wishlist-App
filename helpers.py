import pathlib
import functools
from os import listdir, environ
from os.path import isfile, join

from flask import render_template
from flask_login import current_user

from decorators.auth import ENABLE_INTERNAL_AUTH

from services.email_service import is_email_configured

def get_base_path():
    env = environ.get("BASE_PATH")
    if (env is None):
        return "/"
        
    if (env.endswith("/")):
        return env
        
    return env + "/"

BASE_PATH = get_base_path()

bundle_files_path = 'client/public/build'

def get_bundle_files():
    # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    return [f for f in listdir(bundle_files_path) if isfile(join(bundle_files_path, f))]

def get_css():
    bundle_files = get_bundle_files()
    css_file = list(filter(lambda f: pathlib.Path(f).suffix == '.css', bundle_files))[0]
    return join(BASE_PATH, 'build', css_file)

def get_js():
    bundle_files = get_bundle_files()
    
    def map_file(file: str):
        last_index = file.rindex("-")
        file_dict = {
            file[0:last_index]: join(BASE_PATH, 'build', file)
        }
        return file_dict
    
    def reduce_files(file_a, file_b):
        file_dict = {
            **file_a,
            **file_b
        }
        return file_dict
    
    auto_bundles = dict(
        functools.reduce(
            reduce_files,
            map(
                map_file, 
                filter(lambda f: pathlib.Path(f).suffix == '.js', bundle_files)
            )
        )
    )
    
    return auto_bundles

def custom_render_template(template_name, **context):
    return render_template(
        template_name_or_list=template_name,
        user=current_user,
        internal_login_enabled= None if ENABLE_INTERNAL_AUTH is None or ENABLE_INTERNAL_AUTH.lower() == 'false' else 'true',
        auto_bundles=get_js(),
        module_css=get_css(),
        base_path=BASE_PATH,
        email_is_configured=is_email_configured(),
        **context
    )
