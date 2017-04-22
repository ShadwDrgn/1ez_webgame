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
