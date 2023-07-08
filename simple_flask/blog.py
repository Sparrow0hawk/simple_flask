from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from werkzeug.exceptions import abort

from flask import current_app as app

from simple_flask.auth import login_required
from simple_flask.db import get_db
from .forms import CreatePostForm, EditPostForm, DeletePostForm

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)


@bp.route("/healthcheck")
def healthcheck():
    app.logger.info("Healthcheck ping")
    return "OK"


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    form = CreatePostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data

        error = None

        if not title:
            error = "Title is required"

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id)" " VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            app.logger.info(f"{g.user['id']} created new post.")
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html", form=form)


def get_post(id, check_author=True):
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(id)
    print(post["title"])
    edit_form = EditPostForm(data={"title": post["title"], "body": post["body"]})
    delete_form = DeletePostForm()

    if edit_form.validate_on_submit():
        title = edit_form.title.data
        body = edit_form.body.data
        error = None

        if not title:
            error = "Title is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ?" " WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template(
        "blog/update.html", edit_form=edit_form, delete_form=delete_form, post=post
    )


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))
