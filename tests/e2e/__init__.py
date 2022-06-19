from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

engine = create_engine(f"postgresql://{environ['POSTGRES_USER']}:{environ['POSTGRES_PASSWORD']}@:5432/{environ['POSTGRES_DB']}").connect()

base_url = environ['BASE_URL']
base_add_film = environ['BASE_ADD_FILM']
base_del_film = environ['BASE_DEL_FILM']
base_edit_film = environ['BASE_EDIT_FILM']
