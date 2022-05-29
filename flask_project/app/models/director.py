from app.database.flask_db import db


class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
