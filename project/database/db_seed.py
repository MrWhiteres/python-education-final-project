from os import environ
from sys import platform

import requests
from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.exc import PendingRollbackError, IntegrityError

load_dotenv()


def fake():
    return Faker()


def fake_user(fake=fake()):
    password = fake.password()
    return dict(nickname=fake.unique.first_name(), email=fake.unique.email(), first_name=fake.unique.first_name(),
                last_name=fake.unique.last_name(), password=password, password2=password)


def fake_director(fake=fake()):
    return dict(first_name=fake.unique.first_name(), last_name=fake.unique.last_name())


def session(user=fake_user()):
    session = requests.session()
    session.post(f"{environ['BASE_URL']}/registration", json=user)
    session.post(f'{environ["BASE_URL"]}/login',
                 json=dict(email=user["email"], password=user["password"]))
    print(user)
    return session


def fake_film(fake=fake()):
    while True:
        movie_title = fake.unique.company()
        if len(movie_title) <= 20:
            break

    release_date = "-".join(fake.unique.date().split('/'))
    genre = [fake.unique.first_name() for _ in range(fake.random_digit_not_null())]
    id_director = fake.randomize_nb_elements(number=50, ge=True, min=2)
    description = fake.paragraph(nb_sentences=fake.random_digit_not_null())
    poster = fake.url()
    return dict(movie_title=movie_title, rating=fake.random_digit_not_null(), release_date=release_date,
                genre=genre, id_director=id_director, description=description, poster=poster)


def create_engine_for_db():
    if platform == "linux" or platform == "linux2":
        engine = create_engine(f"postgresql://{environ['POSTGRES_USER']}:" \
                               f"{environ['POSTGRES_PASSWORD']}@{environ['HOST']}:5432/{environ['POSTGRES_DB']}").connect()
    elif platform == "win32":
        engine = create_engine(f"postgresql://{environ['POSTGRES_USER']}:" \
                               f"{environ['POSTGRES_PASSWORD']}@:5432/{environ['POSTGRES_DB']}").connect()
    return engine


def add_director(engine=create_engine_for_db(), director=fake_director()):
    count = 0
    while count < 100:
        try:
            engine.execute(
                f"INSERT INTO movies.public.director(first_name, last_name) VALUES ('{director['first_name']}', '{director['last_name']}')")
            count += 1
            director = fake_director()
            print(1)
        except (IntegrityError, PendingRollbackError):
            director = fake_director()
        print(2)


def add_film(user=session(), film=fake_film()):
    user_film = 0
    count = 0
    while count < 100:
        response = user.post(environ['BASE_ADD_FILM'], json=film)
        if response.status_code == 201:
            user_film += 1
            count += 1
            film = fake_film()
        else:
            film = fake_film()
        if user_film == 10:
            user = session()
            user_film = 0


if __name__ == "__main__":
    add_director()
    add_film()
