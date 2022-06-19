import pytest
import requests
from faker import Faker

from tests.e2e import base_url, engine


@pytest.fixture
def fake():
    yield Faker()


@pytest.fixture
def fake_user(fake):
    password = fake.password()
    yield dict(nickname=fake.unique.first_name(), email=fake.unique.email(), first_name=fake.unique.first_name(),
               last_name=fake.unique.last_name(), password=password, password2=password)


@pytest.fixture
def session():
    yield requests.session()

def delete_user_data_in_db():
    engine.execute("DELETE FROM movies.public.user")

def test_registration(fake_user, session):
    data_registration_good = dict.copy(fake_user)

    data_registration_password = dict.copy(fake_user)
    data_registration_password["password2"] = 'asdasdasd'

    data_registration_field = dict.copy(fake_user)
    data_registration_field["nickname"] = None

    data_registration_validate = dict.copy(fake_user)
    data_registration_validate["email"] = "testerstest.com"

    # Successful user registration test.
    response_good = session.post(f"{base_url}/registration", json=data_registration_good)
    response_user_ex = session.post(f"{base_url}/registration", json=data_registration_good)
    # User registration test in case passwords do not match.
    response_password = session.post(f"{base_url}/registration", json=data_registration_password)
    # Test for the situation when there is no data from the fields.
    response_field = session.post(f"{base_url}/registration", json=data_registration_field)
    # A test in which the user did not pass validation when entering mail data.
    response_validate = session.post(f"{base_url}/registration", json=data_registration_validate)
    # Answer
    assert response_good.status_code == 201
    assert response_user_ex.status_code == 403
    assert response_password.status_code == 409
    assert response_field.status_code == 409
    assert response_validate.status_code == 409

    delete_user_data_in_db()


def test_login(fake_user, session):
    data_registration_good = dict.copy(fake_user)
    session.post(f"{base_url}/registration", json=data_registration_good)

    data_login_good = dict(email=fake_user['email'], password=fake_user["password"])
    data_login_field = dict(email="", password=fake_user["password"])
    data_login_password = dict(email=fake_user['email'], password="123asdasd")

    # Successful user registration.
    response_good = requests.post(f'{base_url}/login', json=data_login_good, allow_redirects=True)
    # The situation in which the email address is not entered.
    response_field = requests.post(f'{base_url}/login', json=data_login_field, allow_redirects=True)
    # A situation in which an incorrect password or email address was entered.
    response_password = requests.post(f'{base_url}/login', json=data_login_password, allow_redirects=True)
    # Answer
    assert response_good.status_code == 200
    assert response_field.status_code == 409
    assert response_password.status_code == 409

    delete_user_data_in_db()


def test_logout(fake_user, session):
    data_registration_good = fake_user
    session.post(f"{base_url}/registration", json=data_registration_good)

    data_login_good = dict(email=fake_user["email"], password=fake_user["password"])
    session.post(f'{base_url}/login', json=data_login_good, allow_redirects=True)

    response = session.post(f'{base_url}/logout')
    assert response.status_code == 200

    bad_logout = session.post(f'{base_url}/logout')
    assert bad_logout.status_code in (401, 403)

    delete_user_data_in_db()
