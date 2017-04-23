from app.database import db


class Terrain(db.Document):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class Location(db.Document):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)
    terrain = db.ReferenceField(Terrain)
    x = db.IntField()
    y = db.IntField()
