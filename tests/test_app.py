from flask import Flask
from app import app


def test_app():
    assert isinstance(app, Flask)
