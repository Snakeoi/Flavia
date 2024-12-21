import importlib
from flask import Flask, Blueprint


def setup_blueprints(app: "Flask", modules: dict[str, tuple[str]]) -> None:
    """Register all blueprints."""
    for module_name, blueprints_names in modules.items():
        module: object = importlib.import_module(f'application.{module_name}')
        for blueprint_name in blueprints_names:
            blueprint: Blueprint = getattr(module, blueprint_name)
            app.register_blueprint(blueprint)
