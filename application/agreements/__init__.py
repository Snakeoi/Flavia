from flask import Blueprint

from . import views

agreements = Blueprint(
    "agreements",
    __name__,
    url_prefix="/agreements",
)

agreements.add_url_rule("/", view_func=views.AgreementsView.as_view("agreements"))

agreements.add_url_rule("/<path:slug>", view_func=views.AgreementView.as_view("agreement"))

agreements.add_url_rule("/<int:id>", view_func=views.AgreementView.as_view("agreement_delete"))
