import time
from .configuration import Configuration
from werkzeug.security import check_password_hash, generate_password_hash
from app import lm, app
from itsdangerous import URLSafeTimedSerializer, BadSignature, BadData
from pymongo import ReturnDocument


class HasAP():
    def __init__(self, ap):
        self.ap = ap
        self.last_ap = Configuration.get_last_tick()

    def set_ap(self, ap=None):
        if ap is not None:
            self.ap = ap
            self.last_ap = Configuration.get_last_tick()
            return

    def get_new_ap(self):
        aprate = Configuration.aprate
        curtick = int(time.time())
        newap = int((curtick - self.last_ap) / aprate)
        return self.ap + newap


class LivingEntity(HasAP):
    def __init__(self, ap, hp):
        HasAP.__init__(self, ap)
        self.hp = hp


class Character(HasAP):
    def __init__(self, ap):
        HasAP.__init__(self, ap)


class User():

    def __init__(self, username):
        u = Configuration.USERS_COLLECTION.find_one({"_id": username})
        self.username = username
        self.charachters = None if 'charachters' not in u else u['characters']
        self.char_count = 0 if self.charachters is None else \
            len(self.charachters)
        self.roles = None if 'roles' not in u else u['roles']
        self.email = None if 'email' not in u else u['email']
        self.confirmed = False if 'confirmed' not in u else u['confirmed']

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def generate_my_token(self):
        return User.generate_token(self.username)

    def set_confirmed(self, is_confirmed):
        self.confirmed = is_confirmed
        self.save()

    def save(self):
        Configuration.USERS_COLLECTION.find_one_and_update(
            {"_id": self.username},
            {
                '$set': {'confirmed': self.confirmed},
                '$set': {'email': self.email}
            }, return_document=ReturnDocument.AFTER)

    @staticmethod
    def add(user, email, password):
        if User.get(user) is None:
            Configuration.USERS_COLLECTION.insert_one(
                {
                    '_id': user,
                    'email': email,
                    'passhash': generate_password_hash(password),
                    'confirmed': False
                })

    @staticmethod
    def generate_token(username):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return serializer.dumps(username,
                                salt=app.config['SECRET_PASSWORD_SALT'])

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

    @staticmethod
    def get(username):
        u = Configuration.USERS_COLLECTION.find_one({"_id": username})
        if not u:
            return None
        return User(u['_id'])

    @staticmethod
    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=app.config['SECRET_PASSWORD_SALT'],
                max_age=expiration
            )
        except (BadSignature, BadData):
            return False
        return email


@lm.user_loader
def load_user(username):
    return User.get(username)
