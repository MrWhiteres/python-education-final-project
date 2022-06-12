import requests
import pytest

base_url = 'http://127.0.0.1'
base_add_film = "http://127.0.0.1/add_film"
base_del_film = "http://127.0.0.1/del_films"
base_edit_film = "http://127.0.0.1/edit/film/"
base_view_film = "http://127.0.0.1/film/"

session_1 = requests.session()
session_2 = requests.session()
session_1.post(f"{base_url}/registration",
               json=dict(nickname="Tester", last_name="Test_name", first_name="Test_last_name",
                         email="tester@test.com", password="test_password",
                         password2="test_password"))
session_2.post(f"{base_url}/registration",
               json=dict(nickname="Testername2", last_name="Test_name", first_name="Test_last_name",
                         email="testergmail@test.com", password="some_password",
                         password2="some_password"))
session_1.post(f'{base_url}/login',
               json=dict(email="tester@test.com",
                         password="test_password"),
               allow_redirects=True)
session_2.post(f'{base_url}/login',
               json=dict(email="testergmail@test.com",
                         password="some_password"),
               allow_redirects=True)


def test_add_film():
    film_good = dict(movie_title='Test film',
                     release_date='2020/02/02',
                     rating=1,
                     poster='Some Poster',
                     description='Some description',
                     genre=0,
                     id_director=[])
    film_bad_title = dict(movie_title='',
                          release_date='2020/02/02',
                          rating=1,
                          poster='Some Poster',
                          description='Some description',
                          genre=0,
                          id_director=0)
    film_bad_data = dict(movie_title='Test film',
                         release_date='2020-02-02',
                         rating=1,
                         poster='Some Poster',
                         description='Some description',
                         genre=0,
                         id_director=0)

    response_s1 = session_1.post(base_add_film, json=film_good)
    assert response_s1.json() == {"answer": f"'{film_good['movie_title']}' created."}
    response_s2 = session_2.post(base_add_film, json=film_good)
    assert response_s2.json() == {"answer": "Film already exist."}
    response_s1 = session_1.post(base_add_film, json=film_bad_title)
    assert response_s1.json() == {"answer": 'Incorrect data'}
    response_s1 = session_1.post(base_add_film, json=film_bad_data)
    assert response_s1.json() == {"answer": 'Incorrect data'}


def test_del_film():
    good_title = dict(movie_title="Test film")
    bad_title = dict(movie_title="Test")
    response_s1 = session_1.post(base_del_film, json=bad_title)
    response_s2 = session_2.post(base_del_film, json=good_title)
    response_s1_2 = session_1.post(base_del_film, json=good_title)
    response_s2_2 = session_2.post(base_del_film, json=good_title)
    assert response_s1.json() == {"answer": f"Film '{bad_title['movie_title']}' not found."}
    assert response_s2.json() == {"answer": f"You can`t delete this film '{good_title['movie_title']}'."}
    assert response_s1_2.json() == {"answer": f"'{good_title['movie_title']}' delete."}
    assert response_s2_2.json() == {"answer": f"Film '{good_title['movie_title']}' not found."}


def test_edit_film():
    film_good = dict(movie_title="Test film", release_date="2020/02/02", rating=3, poster="Some Poster",
                     description="Some description", genre=None, id_director=None)
    session_1.post(base_add_film, json=film_good)
    old_title = film_good['movie_title']
    film_good['movie_title'] = 'Test Film 2'
    del film_good['genre']
    response_1 = session_1.post(f"{base_edit_film}/{old_title}", json=film_good)
    assert response_1.json() == {'Film': 'Movies have been successfully modified'}
    response_2 = session_2.post(f"{base_edit_film}/{film_good['movie_title']}", json=film_good)
    assert response_2.json() == {"Film": "You cannot edit this film."}
    response_3 = session_1.post(f"{base_edit_film}/A_team", json=film_good)
    assert response_3.json() == {'Film': 'Film not Found'}
    session_1.post(f"{base_del_film}", json=film_good)
