import os
from app import app
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
url_db = f"postgresql://{os.environ['POSTGRES_USER']}:" \
         f"{os.environ['POSTGRES_PASSWORD']}@db:5432/{os.environ['POSTGRES_DB']}"
app.config["SQLALCHEMY_DATABASE_URI"] = url_db
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


def init_db():
    """ Creating tables in the database for models from a folder - models."""
    from app.models import director, film, genre, genre_film, role, user
    db.create_all()

