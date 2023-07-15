import os
import tempfile

import multiprocessing
import platform
import socket

import pytest

from typing import Generator, Any
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

from simple_flask import create_app
from simple_flask.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf-8")

# force 'fork' on macOS
if platform.system() == "Darwin":
    multiprocessing.set_start_method("fork")


@pytest.fixture
def app() -> Generator[Flask, Any, Any]:
    db_fnd, db_path = tempfile.mkstemp()

    app = create_app({"TESTING": True, "DATABASE": db_path, "WTF_CSRF_ENABLED": False})

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fnd)
    os.unlink(db_path)


@pytest.fixture
def spawn_app(app):
    # logic for getting random port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    proc = multiprocessing.Process(
        target=app.run,
        kwargs={
            "port": port,
            "host": "127.0.0.1",
            "use_reloader": False,
            "threaded": True,
        },
        daemon=True,
    )
    proc.start()
    yield port
    proc.kill()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="banana"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
