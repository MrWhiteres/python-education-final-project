from . import BaseModel, db


class Genre(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    genre_name = db.Column(db.String(255))

    def __init__(self, genre_name):
        self.genre_name = genre_name

    def __repr__(self):
        return f'<cls-Genre {self.id}>'
