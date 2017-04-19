from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_mail import Mail
from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__)
app.config.from_object('app.game.configuration.Configuration')
app.wsgi_app = ProxyFix(app.wsgi_app)
socketio = SocketIO(app)
lm = LoginManager()
lm.init_app(app)
mail = Mail(app)
lm.login_view = 'login'

from app.views import main
from app.views import usermanagement
from app.sockets import chat
