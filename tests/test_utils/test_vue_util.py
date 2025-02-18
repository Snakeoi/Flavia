import re

from ..fixtures.app_fixtures import app

from application.utils.vue import files


def test_vue_files_detection():
    with app.app_context():
        assets = files.get_assets_files()

        assert re.match(r"^assets/index-.*\.css$", assets["css_file_path"])
        assert re.match(r"^assets/index-.*\.js$", assets["js_file_path"])
