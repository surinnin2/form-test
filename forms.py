from werkzeug.utils import ArgumentValidationError
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, TextAreaField, DateTimeField, validators, SelectField, IntegerField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from datetime import datetime
from models import User, Message

def datetime_check(form, field):
    dt = datetime.datetime
    if field.data < datetime.utcnow():
        raise ValidationError('Must be set to a future time')

class PhoneForm(Form):
    """Subform. CSRF disabled"""

    number = StringField('Phone Number', validators=[validators.InputRequired()])

class MessageForm(FlaskForm):
    """Form for adding messages to que"""

    text = TextAreaField('Message', validators=[DataRequired()])
    datetime = StringField('Time Delivered', validators=[DataRequired()])
    phone_numbers = FieldList(FormField(PhoneForm), min_entries=1, max_entries=20)

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    phone_number = IntegerField('Phone Number')

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])