import pytest
import requests

base_url = "http://127.0.0.1"
session = requests.session()


def test_general_page():
    data = dict(filters="", sorted_methods='', genres=0, paginate=0, director_id=0, min_date='', max_date='')
    response = requests.post(f'{base_url}/1', json=data)
    print(response.json())
    assert response.json() == dict(Film=response.json()['Film'])
