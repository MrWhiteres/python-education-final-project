from logging import getLogger
from flask import Flask

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

from . import routs
from app.database.flask_db import init_db

init_db()

console = getLogger('console')
