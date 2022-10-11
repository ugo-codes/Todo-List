from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TodoForm(FlaskForm):
    todo = StringField(label="", validators=[DataRequired()])
    submit = SubmitField(label="Add")
