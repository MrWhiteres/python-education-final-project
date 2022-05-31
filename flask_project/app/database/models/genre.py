from . import BaseModel, db


class Genre(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    genre_name = db.Column(db.String(255))
