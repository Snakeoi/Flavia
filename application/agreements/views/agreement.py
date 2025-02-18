from flask import views
from flask import request

from application.utils.crud import CommonCRUD
from application.models import Agreement
from .. import schemas


class AgreementsView(views.MethodView):
    def get(self):
        return CommonCRUD.get_all(schemas.AgreementReadSchema, Agreement.query)

    def post(self):
        return CommonCRUD.post(schemas.AgreementCreateSchema, Agreement, request.json)


class AgreementView(views.MethodView):
    def get(self, slug: str):
        return CommonCRUD.get_one(schemas.AgreementReadSchema, Agreement.query.filter_by(slug=slug))

    def put(self, slug: str):
        return CommonCRUD.put(schemas.AgreementEditSchema, Agreement.query.filter_by(slug=slug), request.json)

    def delete(self, id: int):
        return CommonCRUD.delete(Agreement.query.filter_by(slug=id))
