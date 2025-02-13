from flask import Blueprint, render_template, abort


vue = Blueprint("vue", __name__, url_prefix="/", template_folder="templates")


@vue.route("/")
@vue.route("/<path:sub_path>")
def index(sub_path=None):
    """Redirects non API traffic to Vue SPA router."""
    return render_template("vue/index.html")


@vue.route("/api/")
@vue.route("/api/<path:sub_path>")
def api(sub_path=None):
    """Handles API Not Found paths and returns 404. To avoid showing app HTML as response."""
    abort(404)


@vue.route("/static/")
@vue.route("/static/<path:sub_path>")
def static(sub_path=None):
    """Handles static files Not Found paths and returns 404. To avoid showing app HTML as response."""
    abort(404)
