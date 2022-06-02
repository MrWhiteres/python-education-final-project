from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

marsh = Marshmallow()
db = SQLAlchemy()
migrate = Migrate()
