from .config import db
from flask import Flask, Blueprint
from flask_socketio import SocketIO
from werkzeug.contrib.fixers import ProxyFix
from flask_security import Security, MongoEngineUserDatastore
from .account.models.user import User, Role
from flask_mail import Mail
from .account.views.form_extendedlogin import ExtendedLoginForm

# Create app
app = Flask(__name__)

# Load configuration
app.config.from_object('app.config.Configuration')

# Allow for proxy (X-Forwarded-For, etc.)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

# Create socket
socketio = SocketIO(app)

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedLoginForm)


# Initialize database
db.init_app(app)

# Initialize mail
mail = Mail(app)

# Create blueprints
admin_page = Blueprint('admin_page', __name__,
                       template_folder='admin_page/templates')
app.register_blueprint(admin_page, url_prefix='/admin')


from .views import main
from .account.views import account
from .game.views import characters
from .sockets.views import chat
from .admin import admin
