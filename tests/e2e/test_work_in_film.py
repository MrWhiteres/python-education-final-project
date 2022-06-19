import pytest
import requests
from faker import Faker

from tests.e2e import base_url, base_add_film, base_del_film, base_edit_film, engine


def delete_all_data_in_db():
    engine.execute("DELETE FROM movies.public.genre_film")
    engine.execute("DELETE FROM movies.public.film")
    engine.execute("DELETE FROM movies.public.user")


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture
def fake_user_1(fake):
    password = fake.password()
    return dict(nickname=fake.unique.first_name(), email=fake.unique.email(), first_name=fake.unique.first_name(),
                last_name=fake.unique.last_name(), password=password, password2=password)


@pytest.fixture
def fake_user_2(fake):
    password = fake.password()
    return dict(nickname=fake.unique.first_name(), email=fake.unique.email(), first_name=fake.unique.first_name(),
                last_name=fake.unique.last_name(), password=password, password2=password)


@pytest.fixture
def fake_film(fake):
    while True:
        movie_title = fake.unique.company()
        if len(movie_title) <= 20:
            break

    release_date = "-".join(fake.unique.date().split('/'))
    genre = [fake.unique.first_name() for _ in range(fake.random_digit_not_null())]
    id_director = fake.randomize_nb_elements(number=1000, ge=True, min=2)
    description = fake.paragraph(nb_sentences=fake.random_digit_not_null())
    poster = fake.url()
    yield dict(movie_title=movie_title, rating=fake.random_digit_not_null(), release_date=release_date,
               genre=genre, id_director=id_director, description=description, poster=poster)


@pytest.fixture
def session_1(fake_user_1):
    session = requests.session()
    session.post(f"{base_url}/registration", json=fake_user_1)
    session.post(f'{base_url}/login',
                 json=dict(email=fake_user_1["email"], password=fake_user_1["password"]))
    print(fake_user_1)
    yield session


@pytest.fixture
def session_2(fake_user_2):
    session = requests.session()
    session.post(f"{base_url}/registration", json=fake_user_2)
    session.post(f'{base_url}/login',
                 json=dict(email=fake_user_2["email"], password=fake_user_2["password"]))
    print(fake_user_2)
    yield session


def test_add_film(session_1, session_2, fake_film):
    user_1 = session_1
    user_2 = session_2
    film_good = dict.copy(fake_film)
    film_bad_title = dict.copy(fake_film)
    film_bad_title["movie_title"] = ''
    film_bad_data = dict.copy(fake_film)
    film_bad_data["release_date"] = '2020/02/02'

    response_s1 = user_1.post(base_add_film, json=film_good)
    assert response_s1.status_code == 201
    response_s2 = user_2.post(base_add_film, json=film_good)
    assert response_s2.status_code == 409
    user_1.post(base_del_film, json=dict(movie_title=film_good["movie_title"]))
    response_s1 = user_1.post(base_add_film, json=film_bad_title)
    assert response_s1.status_code == 409
    response_s1 = user_2.post(base_add_film, json=film_bad_data)
    assert response_s1.status_code == 409

    delete_all_data_in_db()


def test_del_film(session_1, session_2, fake_film):
    user_1 = session_1
    user_2 = session_2

    user_1.post(base_add_film, json=fake_film)

    good_title = dict(movie_title=fake_film["movie_title"])
    bad_title = dict(movie_title="Test")

    response_s1 = user_1.post(base_del_film, json=bad_title)
    response_s2 = user_2.post(base_del_film, json=good_title)
    response_s1_2 = user_1.post(base_del_film, json=good_title)
    response_s2_2 = user_2.post(base_del_film, json=good_title)

    assert response_s1.status_code == 204
    assert response_s2.status_code == 403
    assert response_s1_2.status_code == 200
    assert response_s2_2.status_code == 204

    delete_all_data_in_db()


def test_edit_film(session_1, session_2, fake_film):
    user_1 = session_1
    user_2 = session_2
    film_good = fake_film
    user_1.post(base_add_film, json=film_good)
    old_title = film_good['movie_title']
    film_good['movie_title'] = Faker().first_name()
    del film_good['genre']
    del film_good['id_director']
    response_1 = user_1.post(f"{base_edit_film}/{old_title}", json=film_good)
    assert response_1.status_code == 200
    response_2 = user_2.post(f"{base_edit_film}/{film_good['movie_title']}", json=film_good)
    assert response_2.status_code == 403
    response_3 = user_1.post(f"{base_edit_film}/A_team", json=film_good)
    assert response_3.status_code == 204
    user_1.post(f"{base_del_film}", json=film_good)

    delete_all_data_in_db()
