from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from werkzeug.exceptions import abort 

from flask import current_app as app

from simple_flask.auth import login_required
from simple_flask.db import get_db

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


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    form = CreatePostForm()
    if form.validate_on_submit():
        flash("Form validated!")
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
                "INSERT INTO post (title, body, author_id)"
                " VALUES (?, ?, ?)",
                (title, body, g.user['id'])
            )
            db.commit()
            app.logger.info(f"{g.user['id']} created new post.")
            return redirect(url_for("blog.index"))
        
    return render_template("blog/create.html", form=form)


class CreatePostForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    body = StringField("body", validators=[DataRequired()])
    submit = SubmitField()
