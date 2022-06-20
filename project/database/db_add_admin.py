from os import environ
from sys import platform

import requests
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


def add_admin(engine=create_engine_for_db()):
    """
    function that add new admin
    :return:
    """
    admin_info = dict(nickname=environ["NICKNAME"], email=environ["EMAIL"], first_name=environ["FIRST_NAME"],
                      last_name=environ["LAST_NAME"], password=environ["PASSWORD"], password2=environ["PASSWORD2"])

    response = requests.session().post(f"{environ['BASE_URL']}/registration", json=admin_info)
    engine.execute(
        f"UPDATE movies.public.user set id_role = (select id from role where role_name='admin') where nickname='{environ['NICKNAME']}'")
    if response.status_code == 201:
        print("Administrator created.")
    else:
        print('Administrator already exists with this data')


if __name__ == "__main__":
    add_admin()
