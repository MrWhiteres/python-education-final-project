from logging import getLogger

from .app import app
from .database import db, migrate, marsh

console = getLogger('console')


@app.before_first_request
def init_db():
    """ Creating tables in the database for models from a folder - models."""
    from .database.models import director, user, film, genre, genre_film, role
    db.init_app(app)
    migrate.init_app(app, db)
    marsh.init_app(app)
    db.create_all()
