from os import environ
from sys import platform

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def create_engine_for_db():
    if platform == "linux" or platform == "linux2":
        engine = create_engine(f"postgresql://{environ['POSTGRES_USER']}:" \
                               f"{environ['POSTGRES_PASSWORD']}@{environ['HOST']}:5432/{environ['POSTGRES_DB']}").connect()
    elif platform == "win32":
        engine = create_engine(f"postgresql://{environ['POSTGRES_USER']}:" \
                               f"{environ['POSTGRES_PASSWORD']}@:5432/{environ['POSTGRES_DB']}").connect()
    return engine


engine = create_engine_for_db()

base_url = environ['BASE_URL']
base_add_film = environ['BASE_ADD_FILM']
base_del_film = environ['BASE_DEL_FILM']
base_edit_film = environ['BASE_EDIT_FILM']
