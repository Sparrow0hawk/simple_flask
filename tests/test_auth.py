import pytest

from flask import g, session
from simple_flask.db import get_db


def test_register(client, app):
    assert client.get("/auth/register").status_code == 200

    res = client.post("/auth/register", data={"username": "boo", "password": "spooky"})
    assert res.headers["Location"] == "/auth/login"

    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM user WHERE username = 'boo'").fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required"),
        ("boo", "", b"Password is required"),
        ("test", "test", b"User test is already registered"),
    ),
)
def test_register_validate_input(client, username, password, message):
    res = client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    assert message in res.data


def test_login(client, auth):
    assert client.get("/auth/login").status_code == 200
    res = auth.login()
    assert res.headers["Location"] == "/"

    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user["username"] == "test"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("a", "test", b"Incorrect username"),
        ("test", "a", b"Incorrect password"),
    ),
)
def test_login_validate_input(auth, client, username, password, message):
    res = auth.login(username, password)
    assert message in res.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
