"""
Module stores the object model director.
"""
from . import BaseModel
from ...database import db


class Director(db.Model, BaseModel):
    """
    Class is the schema for the director model.
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f'<cls-Director {self.id}, ({self.first_name}, {self.last_name}).>'
