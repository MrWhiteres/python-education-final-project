from datetime import datetime

from . import BaseModel, db


class Film(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    movie_title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.DateTime, default=datetime.utcnow)
    poster = db.Column(db.Text)
    id_director = db.Column(db.Integer, db.ForeignKey("director.id"))
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
