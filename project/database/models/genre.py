"""
Module stores the object model genre.
"""
from . import BaseModel, db


class Genre(db.Model, BaseModel):
    """
    Class is the schema for the genres table.
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    genre_name = db.Column(db.String(255), unique=True)

    def __init__(self, genre_name):
        self.genre_name = genre_name

    def __repr__(self):
        return f'<cls-Genre {self.id}>'
