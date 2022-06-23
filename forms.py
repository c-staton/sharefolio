from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import Email, InputRequired
from wtforms.widgets import PasswordInput

class RegisterForm(FlaskForm):
    """Form for registering new users"""

    email = StringField('Email', validators=[Email('Must enter valid email'), InputRequired()])

    username = StringField('Username', validators=[InputRequired()])

    password = StringField('Password', widget=PasswordInput(hide_value=False))


class LoginForm(FlaskForm):
    """Form for loggin in a user"""

    username = StringField('Username', validators=[InputRequired()])

    password = StringField('Password', widget=PasswordInput(hide_value=False))

class AddSharesForm(FlaskForm):
    """Form for users to add more shares to portfolio"""

    symbol = StringField('Symbol', validators=[InputRequired()])

    shares = DecimalField('Shares', validators=[InputRequired()])