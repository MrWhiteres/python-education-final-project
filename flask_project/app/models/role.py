from app.database.flask_db import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    role_name = db.Column(db.String(255))
