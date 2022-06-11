from logging import getLogger

from .app import app, db
from .database import marsh

console = getLogger('console')


@app.before_first_request
def init_db():
    """ Creating tables in the database for models from a folder - models."""
    from .database.models import director, user, film, genre, genre_film, role
    marsh.init_app(app)
    db.create_all()
