from flask_security.forms import ConfirmRegisterForm
from wtforms import StringField
from wtforms.validators import InputRequired


class ExtendedLoginForm(ConfirmRegisterForm):
    username = StringField('Username', [InputRequired()])
