"""
Module that creates a flask application.
"""
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_pyfile('config.py')
login_manager = LoginManager(app)
csrf = CSRFProtect(app)

from . import routs
