from typing import Any

from flask_marshmallow import Schema
from marshmallow import validate
from marshmallow import fields


class UnsupportedValidatorError(Exception):

    def __init__(self, validator: str) -> None:
        self.message = f"unsupported validator: {type(validator)}"
        super().__init__(self.message)


class UnsupportedFieldError(Exception):

    def __init__(self, validator: str) -> None:
        self.message = f"unsupported field: {type(validator)}"
        super().__init__(self.message)


def serialize_requirements(validator: Any) -> dict[str, Any]:
    serializers: dict = {
        validate.URL: lambda v: {
            "type": "url",
            "error": v.error,
        },
        validate.Email: lambda v: {
            "type": "email",
            "error": v.error,
        },
        validate.Range: lambda v: {
            "type": "range",
            "min": v.min,
            "max": v.max,
            "min_inclusive": v.min_inclusive,
            "max_inclusive": v.max_inclusive,
        },
        validate.Length: lambda v: {
            "type": "length",
            "min": v.min,
            "max": v.max,
            "equal": v.equal,
            "error": v.error,
        },
        validate.Equal: lambda v: {
            "type": "equal",
            "comparable": v.comparable,
            "error": v.error,
        },
        validate.Regexp: lambda v: {
            "type": "regex",
            "regex": v.regex.pattern,
            "error": v.error,
        },
        validate.NoneOf: lambda v: {
            "type": "none_of",
            "iterable": list(v.iterable),
            "error": v.error,
        },
        validate.OneOf: lambda v: {
            "type": "one_of",
            "choices": list(v.choices),
            "labels": list(v.labels),
            "error": v.error,
        },
    }

    serialize = serializers.get(type(validator), None)
    if serialize is None:
        raise UnsupportedValidatorError(validator)
    else:
        return serialize(validator)


def serialize_field_type(field: Any) -> str:
    serializers = {
        fields.Raw: "Raw",
        fields.Nested: "Nested",
        fields.Mapping: "Mapping",
        fields.Dict: "Dict",
        fields.List: "List",
        fields.Tuple: "Tuple",
        fields.String: "String",
        fields.UUID: "UUID",
        fields.Number: "Number",
        fields.Integer: "Integer",
        fields.Decimal: "Decimal",
        fields.Boolean: "Boolean",
        fields.Float: "Float",
        fields.DateTime: "DateTime",
        fields.NaiveDateTime: "NaiveDateTime",
        fields.AwareDateTime: "AwareDateTime",
        fields.Time: "Time",
        fields.Date: "Date",
        fields.TimeDelta: "TimeDelta",
        fields.Url: "Url",
        fields.URL: "URL",
        fields.Email: "Email",
        fields.IP: "IP",
        fields.IPv4: "IPv4",
        fields.IPv6: "IPv6",
        fields.IPInterface: "IPInterface",
        fields.IPv4Interface: "IPv4Interface",
        fields.IPv6Interface: "IPv6Interface",
        fields.Enum: "Enum",
        fields.Method: "Method",
        fields.Function: "Function",
        fields.Str: "Str",
        fields.Bool: "Bool",
        fields.Int: "Int",
        fields.Constant: "Constant",
        fields.Pluck: "Pluck",
    }
    serialize = serializers.get(type(field), None)
    if serialize is None:
        raise UnsupportedFieldError(field)
    else:
        return serialize


def serialize_schema(schema: Schema):

    result = {}
    for key, value in schema.fields.items():
        if value.validate:
            if isinstance(value.validate, list):

                validators = [
                    serialize_requirements(validator)
                    for validator in value.validate]
            else:
                validators = serialize_requirements(value.validate)

            result[key] = {
                "type": serialize_field_type(value),
                "required": value.required,
                "validators": validators,
            }

    return result
