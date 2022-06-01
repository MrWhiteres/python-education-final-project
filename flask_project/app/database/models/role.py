from . import BaseModel, db


class Role(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    role_name = db.Column(db.String(255), unique=True)

    def __init__(self, role_name):
        self.role_name = role_name

    def __repr__(self):
        return f'<cls-Role {self.id}>'
