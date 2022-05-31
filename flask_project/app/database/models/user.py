from flask_login import UserMixin

from . import db, BaseModel


class User(db.Model, BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nickname = db.Column(db.String(255), nullable=False, unique=True)
    last_name = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    id_role = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role")

    def __init__(self, nickname, last_name, first_name, email, password):
        self.nickname = nickname
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.password = password
        self.id_role = None
