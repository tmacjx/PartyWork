from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, Email, DataRequired, Regexp, EqualTo, ValidationError


class CommentForm(Form):
    content = StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit')
