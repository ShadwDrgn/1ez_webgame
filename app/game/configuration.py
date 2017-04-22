import time
from pymongo import MongoClient


class Configuration():
    mongo_client = MongoClient()
    mongo_db = mongo_client['1ez_webgame']
    aprate = 15
    SECRET_KEY = 'LONGWORDSHERE'
    SECRET_PASSWORD_SALT = 'Dis_be-a secret&thang'
    USERS_COLLECTION = mongo_db['users']
    MONGODB_DB = '1ez_webgame'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    SECURITY_USER_IDENTITY_ATTRIBUTES = ('username', 'email')
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_EMAIL_SENDER = 'webgame@1ez.us'
    SECURITY_LOGIN_USER_TEMPLATE = 'account/login.html'
    SECURITY_PASSWORD_SALT = 'TOTALLY RANDOM SHIT IS HERE YOU BITCH!'
    SECURITY_CONFIRMABLE = True

    @staticmethod
    def get_last_tick():
        return int(time.time() / Configuration.aprate) * Configuration.aprate
