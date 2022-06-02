"""
Module that creates a flask application.
"""
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('config.py')
login_manager = LoginManager(app)

from . import routs
