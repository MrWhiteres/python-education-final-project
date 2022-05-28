from logging import getLogger
from flask import Flask


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
from . import ip_user

console = getLogger('console')
