"""
Module that creates a flask application.
"""
from flask import Flask
from flask_login import LoginManager
from flask_restx import Api
from flask_wtf.csrf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension

from .config import BaseConfig
from .database import db, migrate, marsh
from .logger import InterceptHandler

app = Flask(__name__)
api = Api(doc='/swagger', version='1.0', title='Flask-Restx Project', description='by MrWhiteres')

app.config.from_object(BaseConfig)
app.logger.addHandler(InterceptHandler())
dtb = DebugToolbarExtension()

login_manager = LoginManager(app)
csrf = CSRFProtect(app)
db.init_app(app)
migrate.init_app(app, db, directory='./migration')
api.init_app(app)

from .database.models import director, user, film, genre, genre_film, role

marsh.init_app(app)
db.create_all(app=app)

from . import routs
