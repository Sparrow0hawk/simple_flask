from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CreatePostForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    body = TextAreaField("body", validators=[DataRequired()])
    submit = SubmitField()
