"""
Module stores the object model films.
"""
from . import BaseModel, db, marsh
from .genre_film import genre_film
from .genre import Genre
from .director import Director
from .user import User


class Film(db.Model, BaseModel):
    """
    Class is the schema for the movie table.
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    movie_title = db.Column(db.String(255), nullable=False, unique=True)
    release_date = db.Column(db.Date)
    rating = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.Text)
    description = db.Column(db.Text)

    id_director = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship('Director')

    id_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship('User')

    id_genre = db.relationship("Genre", secondary=genre_film)

    def __init__(self, movie_title, release_date, rating, poster=None, description=None, id_director=None, id_user=None):
        self.movie_title = movie_title
        self.release_date = release_date
        self.rating = rating
        self.poster = poster
        self.description = description
        self.id_director = id_director
        self.id_user = id_user

    def __repr__(self):
        return f'<cls-Film: {self.id}/{self.movie_title}/{self.id_user}>'

