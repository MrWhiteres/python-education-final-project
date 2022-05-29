from app.database.flask_db import db


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    genre_name = db.Column(db.String(255))
