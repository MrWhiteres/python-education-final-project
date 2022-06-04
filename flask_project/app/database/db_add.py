"""
Module will be responsible for filling the database with custom values.
"""
from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, PendingRollbackError

load_dotenv()


def add_inform():
    """
    function that performs the role of filling data.
    :return:
    """
    engine = create_engine(f"postgresql://{environ['POSTGRES_USER']}:" \
         f"{environ['POSTGRES_PASSWORD']}@:5432/{environ['POSTGRES_DB']}").connect()
    try:
        engine.execute("INSERT INTO movies.public.role(role_name) VALUES ('user'), ('admin')")
    except (IntegrityError, PendingRollbackError):
        print('Error')


add_inform()