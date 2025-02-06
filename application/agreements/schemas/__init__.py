from application.extensions import ma
from application.models import Agreement


class AgreementReadSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Agreement

    id = ma.auto_field()
    slug = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()


class AgreementCreateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Agreement

    slug = ma.auto_field(required=True)
    name = ma.auto_field(required=True)
    description = ma.auto_field(required=True)


class AgreementEditSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Agreement

    slug = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()