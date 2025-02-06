from typing import Any

from flask import jsonify, abort

from application.extensions import db
from application.extensions import ma

class CommonCRUD:

    @classmethod
    def get_all(cls, schema: "ma.Schema", query: "db.Query"):
        return jsonify(schema.dump(query.all(), many=True))

    @classmethod
    def get_one(cls, schema: "ma.Schema", query: "db.Query"):
        instance = query.one_or_none()
        if instance is None:
            abort(404)
        return jsonify(schema.dump(instance))

    @classmethod
    def post(cls, schema: "ma.Schema", model: "db.Model", data: dict[str: Any]):
        instance = model(**schema.load(data))
        db.session.add(instance)
        db.session.commit()
        return jsonify(schema.dump(instance)), 201

    @classmethod
    def put(cls,  schema: "ma.Schema", query: "db.Query", data: dict[str: Any]):
        instance = query.one_or_none()
        if instance is None:
            abort(404)
        data = schema.load(data)
        for key in data.keys():
            setattr(instance, key, data[key])
        db.session.commit()
        return jsonify(schema.dump(instance))

    @classmethod
    def patch(cls,  schema: "ma.Schema", query: "db.Query", data: dict[str: Any]):
        return cls.put(schema, query, data)

    @classmethod
    def delete(cls, query: "db.Query"):
        instances = query.all()
        if len(instances) == 0:
            abort(404)
        for instance in instances:
            db.session.delete(instance)
        db.session.commit()
        return jsonify(), 204
