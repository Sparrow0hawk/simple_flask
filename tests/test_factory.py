from simple_flask import create_app
from flask.testing import FlaskClient


def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_hello(client: FlaskClient):
    res = client.get("/healthcheck")
    assert res.status_code == 200
