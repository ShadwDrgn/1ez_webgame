import time
from pymongo import MongoClient


class Configuration():
    mongo_client = MongoClient()
    mongo_db = mongo_client['1ez_webgame']
    aprate = 15
    SECRET_KEY = 'LONGWORDSHERE'
    SECRET_PASSWORD_SALT = 'Dis_be-a secret&thang'
    USERS_COLLECTION = mongo_db['users']

    @staticmethod
    def get_last_tick():
        return int(time.time() / Configuration.aprate) * Configuration.aprate
