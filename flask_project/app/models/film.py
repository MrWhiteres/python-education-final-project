from datetime import datetime
from app.database.flask_db import db
from app.models.genre_film import genre_film


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    movie_title = db.Column(db.String(255))
    release_date = db.Column(db.DateTime, default=datetime.utcnow)
    poster = db.Column(db.Text)
    id_director = db.Column(db.Integer, db.ForeignKey("director.id"))
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))

    genre = db.relationship("genre", secondary=genre_film)
