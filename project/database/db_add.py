"""
Module will be responsible for filling the database with custom values.
"""
from os import environ
from sys import platform

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, PendingRollbackError

load_dotenv()


def create_engine_for_db():
    if platform == "linux" or platform == "linux2":
        engine = create_engine(f"postgresql://{environ['POSTGRES_USER']}:" \
                               f"{environ['POSTGRES_PASSWORD']}@{environ['HOST']}:5432/{environ['POSTGRES_DB']}").connect()
    elif platform == "win32":
        engine = create_engine(f"postgresql://{environ['POSTGRES_USER']}:" \
                               f"{environ['POSTGRES_PASSWORD']}@:5432/{environ['POSTGRES_DB']}").connect()
    return engine


def add_role(engine=create_engine_for_db()):
    """
    function that performs the role of filling data.
    :return:
    """
    try:
        engine.execute("INSERT INTO movies.public.role(role_name) VALUES ('user'), ('admin')")
    except (IntegrityError, PendingRollbackError):
        print('Data in Role user already been loaded')


def add_genre(engine=create_engine_for_db()):
    """
    function that performs the genre of filling data.
    :return:
    """
    try:
        engine.execute("INSERT INTO movies.public.genre(genre_name) VALUES ('unknown')")
    except (IntegrityError, PendingRollbackError):
        print('Data in genre already been loaded')


def add_director(engine=create_engine_for_db()):
    """
    function that performs the director of filling data.
    :return:
    """
    try:
        engine.execute("INSERT INTO movies.public.director(first_name, last_name) VALUES ('unknown', 'unknown')")
    except (IntegrityError, PendingRollbackError):
        print('Data in director already been loaded')


if __name__ == "__main__":
    add_genre()
    add_director()
    add_role()
