import pytest
from marshmallow import validate, fields
from application.utils.schema_serialization import (
    serialize_requirements,
    serialize_field_type,
    serialize_schema,
    UnsupportedValidatorError,
    UnsupportedFieldError,
)
from flask_marshmallow import Schema

def test_serialize_requirements_handles_supported_validators():
    assert serialize_requirements(validate.URL()) == {"type": "url", "error": "Not a valid URL."}
    assert serialize_requirements(validate.Email()) == {"type": "email", "error": "Not a valid email address."}
    assert serialize_requirements(validate.Range(min=1, max=10)) == {
        "type": "range",
        "min": 1,
        "max": 10,
        "min_inclusive": True,
        "max_inclusive": True,
    }

def test_serialize_requirements_raises_error_for_unsupported_validator():
    with pytest.raises(UnsupportedValidatorError):
        serialize_requirements("unsupported_validator")

@pytest.mark.parametrize(
    "field, expected",
    [
        (fields.Raw(), "Raw"),
        # (fields.Nested(), "Nested"),
        (fields.Mapping(), "Mapping"),
        (fields.Dict(), "Dict"),
        # (fields.List(), "List"),
        # (fields.Tuple(), "Tuple"),
        (fields.String(), "String"),
        (fields.UUID(), "UUID"),
        (fields.Number(), "Number"),
        (fields.Integer(), "Integer"),
        (fields.Decimal(), "Decimal"),
        (fields.Boolean(), "Boolean"),
        (fields.Float(), "Float"),
        (fields.DateTime(), "DateTime"),
        (fields.NaiveDateTime(), "NaiveDateTime"),
        (fields.AwareDateTime(), "AwareDateTime"),
        (fields.Time(), "Time"),
        (fields.Date(), "Date"),
        (fields.TimeDelta(), "TimeDelta"),
        (fields.Url(), "Url"),
        (fields.URL(), "Url"),
        (fields.Email(), "Email"),
        (fields.IP(), "IP"),
        (fields.IPv4(), "IPv4"),
        (fields.IPv6(), "IPv6"),
        (fields.IPInterface(), "IPInterface"),
        (fields.IPv4Interface(), "IPv4Interface"),
        (fields.IPv6Interface(), "IPv6Interface"),
        # (fields.Enum(), "Enum"),
        (fields.Method(), "Method"),
        (fields.Function(), "Function"),
        (fields.Str(), "String"),
        (fields.Bool(), "Boolean"),
        (fields.Int(), "Integer"),
        # (fields.Constant(), "Constant"),
        # (fields.Pluck(), "Pluck"),
    ],
)
def test_serialize_field_type_handles_supported_fields(field, expected):
    assert serialize_field_type(field) == expected

def test_serialize_field_type_raises_error_for_unsupported_field():
    with pytest.raises(UnsupportedFieldError):
        serialize_field_type("unsupported_field")

class ExampleSchema(Schema):
        name = fields.String(required=True, validate=[validate.Length(min=1, max=100)])
        age = fields.Integer(required=True, validate=validate.Range(min=0, max=120))
        email = fields.Email(required=True, validate=validate.Email())
        website = fields.Url(required=False, validate=validate.URL())

def test_serialize_schema_handles_valid_schema():
    schema = ExampleSchema()
    result = serialize_schema(schema)
    assert result == {
        "name": {
            "name": "name",
            "type": "String",
            "required": True,
            "validators": [
                {"type": "length", "min": 1, "max": 100, "equal": None, "error": None}
            ],
        },
        "age": {
            "name": "age",
            "type": "Integer",
            "required": True,
            "validators": {
                "type": "range",
                "min": 0,
                "max": 120,
                "min_inclusive": True,
                "max_inclusive": True,
            },
        },
        "email": {
            "name": "email",
            "type": "Email",
            "required": True,
            "validators": {
                "type": "email",
                "error": "Not a valid email address.",
            },
        },
        "website": {
            "name": "website",
            "type": "Url",
            "required": False,
            "validators": {
                "type": "url",
                "error": "Not a valid URL.",
            },
        },
    }