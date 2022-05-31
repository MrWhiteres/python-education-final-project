from logging import getLogger

from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('config.py')

from . import routs
from .database import db, migrate

login_manager = LoginManager(app)

console = getLogger('console')


@app.before_first_request
def init_db():
    """ Creating tables in the database for models from a folder - models."""
    from .database.models import director, user, film, genre, genre_film, role
    db.init_app(app)
    migrate.init_app(app, db, directory='migrations/')
    db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return user.User.query.get(user_id)
