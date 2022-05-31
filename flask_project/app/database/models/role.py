from . import BaseModel, db


class Role(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    role_name = db.Column(db.String(255))
