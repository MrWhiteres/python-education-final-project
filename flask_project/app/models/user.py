from app.database.flask_db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nickname = db.Column(db.String(255), unique=True)
    last_name = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    id_role = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role")
