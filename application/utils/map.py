from flask import jsonify, current_app


def view():
    return jsonify(
        [
            {"endpoint": rule.endpoint, "url": rule.rule, "method": [method for method in rule.methods]}
            for rule in current_app.url_map.iter_rules()
        ]
    )
