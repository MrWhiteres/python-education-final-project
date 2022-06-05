"""
Module that creates a flask application.
"""
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from .database import db, migrate
from .logger import InterceptHandler

app = Flask(__name__)

app.config.from_pyfile('config.py')
app.logger.addHandler(InterceptHandler())

login_manager = LoginManager(app)
csrf = CSRFProtect(app)
db.init_app(app)
migrate.init_app(app, db)

from . import routs
