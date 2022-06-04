from flask_marshmallow.sqla import SQLAlchemyAutoSchema

from ...database.models.film import Film


class FilmSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Film
        include_relationship = True
        load_instance = True
