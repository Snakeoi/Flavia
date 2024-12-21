import re
import os

from flask import current_app


def get_assets_files():
    assets_path = 'assets/'
    assets: list = os.listdir(os.path.join(current_app.config['BASEDIR'], 'static/' + assets_path))
    css_file_name = [el for el in assets if re.match(r"^index-.*\.css$", el)][0]
    js_file_name = [el for el in assets if re.match(r"^index-.*\.js$", el)][0]

    return dict(
        css_file_path=assets_path + css_file_name,
        js_file_path=assets_path + js_file_name
    )