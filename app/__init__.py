from app.database import db
from flask import Flask
from flask_socketio import SocketIO
from werkzeug.contrib.fixers import ProxyFix
from flask_security import Security, MongoEngineUserDatastore
from app.game.user import User, Role
from flask_mail import Mail
from app.views.forms.extendedlogin import ExtendedLoginForm

# Create app
app = Flask(__name__)

# Load configuration
app.config.from_object('app.game.configuration.Configuration')

# Allow for proxy (X-Forwarded-For, etc.)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Create socket
socketio = SocketIO(app)

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedLoginForm)


# Initialize database
db.init_app(app)

# Initialize mail
mail = Mail(app)


from app.views import main
from app.views import account
from app.sockets import chat
