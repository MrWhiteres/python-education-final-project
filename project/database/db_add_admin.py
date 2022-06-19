from os import environ

import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, PendingRollbackError

load_dotenv()

engine = create_engine(f"postgresql://{environ['POSTGRES_USER']}:" \
                       f"{environ['POSTGRES_PASSWORD']}@:5432/{environ['POSTGRES_DB']}").connect()


def add_admin():
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


add_admin()
