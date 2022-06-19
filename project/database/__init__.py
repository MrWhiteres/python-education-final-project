"""
Module is responsible for creating a database of work on the database and creating migrations.
"""

from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

marsh = Marshmallow()
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect
