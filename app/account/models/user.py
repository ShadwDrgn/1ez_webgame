from app.config import db
from app.game.models.character import Character
from flask_security import UserMixin, RoleMixin
import datetime


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    testattr = db.StringField(max_length=255, default='test')
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    creation_date = db.DateTimeField()
    last_seen = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    characters = db.ListField(db.ReferenceField(Character), default=[])
    username = db.StringField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        return super(User, self).save(*args, **kwargs)
