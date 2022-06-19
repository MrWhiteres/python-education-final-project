import pytest
import requests

from tests.e2e import base_url


@pytest.fixture
def base_data():
    yield base_url


def test_general_page(base_data):
    data = dict(filters=[], sorted_methods=[], genres=[], paginate=0, director_id=[],
                min_date="", max_date="")
    response = requests.post(f'{base_data}', json=data)
    assert response.status_code in (204, 200)
