import time
from app.config import Configuration


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
