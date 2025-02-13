from flask import Blueprint

from . import views

agreement = Blueprint(
    "agreements",
    __name__,
    url_prefix="/agreements",
)

agreement.add_url_rule("/", view_func=views.AgreementsView.as_view("agreements"))

agreement.add_url_rule("/<path:slug>", view_func=views.AgreementView.as_view("agreement"))

agreement.add_url_rule("/<int:id>", view_func=views.AgreementView.as_view("agreement_delete"))
