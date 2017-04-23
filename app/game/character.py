from app.database import db
from .location import Location


class Character(db.Document):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255, default="Default Description")
    location = db.ReferenceField(Location)
    hp = db.IntField()
