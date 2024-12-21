from application.utils import vue


def setup_injects(app):

    @app.context_processor
    def get_vue_asset_files():
        return vue.files.get_assets_files()
