from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Login form to access writing and settings pages"""

    username = StringField('username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('password', validators=[DataRequired()], render_kw={"placeholder": "Password"})


class RegisterForm(FlaskForm):
    """Login form to access writing and settings pages"""

    username = StringField('username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    email = StringField('email', validators=[DataRequired()], render_kw={"placeholder": "email"})
    password = PasswordField('password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
