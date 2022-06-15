"""
Module works it is not possible to create automatic schemas
 for displaying in Json format information from the database
"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from ..models.film import Film
from ..models.user import User


class FilmSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Film
        include_relationship = True
        load_instance = True


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationship = True
        load_instance = True
