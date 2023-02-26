from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Email, Length, email_validator


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class SelectForm(FlaskForm):
    """Form for selectting categories"""
    category = SelectMultipleField('Categories', coerce=int)

class SourceForm(FlaskForm):
    """Form for selecting sources"""

    source = SelectMultipleField('Sources', coerce=int)
