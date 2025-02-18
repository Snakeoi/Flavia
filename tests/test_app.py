from flask import Flask
from app import app
from application import create_app

def test_app():
    assert isinstance(app, Flask)
    assert isinstance(create_app("testing"), Flask)

