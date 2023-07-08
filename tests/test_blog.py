import pytest

from simple_flask.db import get_db


def test_index(client, auth):
    res = client.get("/")

    assert b"Log In" in res.data
    assert b"Register" in res.data

    auth.login()

    res = client.get("/")

    assert b"Log Out" in res.data
    assert b"test title" in res.data
    assert b"by test on 2023-07-07" in res.data
    assert b"test\nbody" in res.data
    assert b'href="/1/update"' in res.data


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
        "/1/delete",
    ),
)
def test_login_required(client, path):
    res = client.post(path)
    assert res.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth):
    with app.app_context():
        db = get_db()
        db.execute("UPDATE post SET author_id = 2 WHERE id = 1")
        db.commit()

    auth.login()

    assert client.post("/1/update").status_code == 403
    assert client.post("/1/delete").status_code == 403

    assert b'href="/1/update"' not in client.get("/").data


@pytest.mark.parametrize(
    "path",
    (
        "/2/update",
        "/2/delete",
    ),
)
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404
