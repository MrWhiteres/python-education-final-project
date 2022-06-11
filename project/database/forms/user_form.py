from wtforms.fields import EmailField

from . import FlaskForm
from . import StringField, PasswordField, validators


class RegistrationForm(FlaskForm):
    nickname = StringField("nickname", validators=[validators.InputRequired(), validators.Length(min=4, max=15)])
    last_name = StringField("last_name", validators=[validators.InputRequired(), validators.Length(min=2, max=35)])
    first_name = StringField("first_name", validators=[validators.InputRequired(), validators.Length(min=2, max=35)])
    email = EmailField('Email Address',
                       [validators.DataRequired(), validators.Email(), validators.Length(min=6, max=35)])
    password = PasswordField('password', validators=[validators.DataRequired(), validators.Length(min=8, max=15)])
    password2 = PasswordField('password2', validators=[validators.InputRequired(), validators.Length(min=8, max=15)])

class LoginForm(FlaskForm):
    email = EmailField('Email Address',
                       [validators.DataRequired(), validators.Email(), validators.Length(min=6, max=35)])
    password = PasswordField('password', validators=[validators.DataRequired(), validators.Length(min=8, max=15)])