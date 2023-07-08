import sqlite3

from typing import BinaryIO

import click
from flask import current_app, g, Flask


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None) -> None:
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()

    current_app: Flask
    f: BinaryIO

    with current_app.open_resource("schema.sql", mode="rb") as f:
        f_bytes = f.read()
        db.executescript(f_bytes.decode("utf-8"))


@click.command("init-db")
def init_db_command() -> None:
    init_db()
    click.echo("Initializing database.")


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
