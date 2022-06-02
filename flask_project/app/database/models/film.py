from datetime import datetime

from . import BaseModel, db, marsh
from .genre_film import genre_film
from .genre import Genre


class Film(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    movie_title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.Text)
    description = db.Column(db.Text)
    id_director = db.Column(db.Integer, db.ForeignKey("director.id"))
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    id_genre = db.relationship("Genre", secondary=genre_film)

    def __init__(self, movie_title, release_date, rating, poster=None, description=None, id_director=None, id_user=None,
                 id_genre=[]):
        self.movie_title = movie_title
        self.release_date = release_date
        self.rating = rating
        self.poster = poster
        self.description = description
        self.id_director = id_director
        self.id_user = id_user
        self.id_genre = id_genre

    def __repr__(self):
        return f'<cls-Film: {self.id}/{self.movie_title}/{self.id_user}>'


class FilmSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Film
