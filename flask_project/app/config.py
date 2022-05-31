from os import environ
from dotenv import load_dotenv

load_dotenv()
JSON_AS_ASCII = False
url_db = f"postgresql://{environ['POSTGRES_USER']}:" \
         f"{environ['POSTGRES_PASSWORD']}@db:5432/{environ['POSTGRES_DB']}"
SQLALCHEMY_DATABASE_URI = url_db
SQLALCHEMY_TRACK_MODIFICATION = False
SECRET_KEY = environ['SECRET_KEY']
