import requests
import pytest


base_url = "http://127.0.0.1"
session = requests.session()


def test_registration():
    data_registration_good = dict(nickname="Tester01", last_name="Test_name", first_name="Test_last_name",
                                  email="testersad@test.com", password="test_password",
                                  password2="test_password")

    data_registration_password = dict(nickname="tester", last_name="Test_name", first_name="Test_last_name",
                                      email="testers@test.com", password="test_password",
                                      password2="test_password1")

    data_registration_field = dict(nickname="", last_name="Test_name", first_name="Test_last_name",
                                   email="testers@test.com", password="test_password",
                                   password2="test_password")

    data_registration_validate = dict(nickname="tester", last_name="test_name", first_name="test_last_name",
                                      email="testerstest.com", password="test_password",
                                      password2="test_password")
    # Successful user registration test.
    response_good = session.post(f"{base_url}/registration", json=data_registration_good)
    # User registration test in case passwords do not match.
    response_password = session.post(f"{base_url}/registration", json=data_registration_password)
    # Test for the situation when there is no data from the fields.
    response_field = session.post(f"{base_url}/registration", json=data_registration_field)
    # A test in which the user did not pass validation when entering mail data.
    response_validate = session.post(f"{base_url}/registration", json=data_registration_validate)
    # Answer
    assert response_good.json() == dict(answer=f"'{data_registration_good['nickname']}' created.")
    assert response_password.json() == dict(answer='Passwords are not equal!')
    assert response_field.json() == dict(answer='Please, fill all fields!')
    assert response_validate.json() == dict(answer='Incorrect data')

def test_login():
    data_login_good = dict(email="tester@test.com", password="test_password")
    data_login_field = dict(email="", password="test_password")
    data_login_password = dict(email="tester@test.com", password="123asdasd")

    # Successful user registration.
    response_good = requests.post(f'{base_url}/login', json=data_login_good, allow_redirects=True)
    # The situation in which the email address is not entered.
    response_field = requests.post(f'{base_url}/login', json=data_login_field, allow_redirects=True)
    # A situation in which an incorrect password or email address was entered.
    response_password = requests.post(f'{base_url}/login', json=data_login_password, allow_redirects=True)
    # Answer
    assert response_good.json() == dict(answer="Welcome back.")
    assert response_field.json() == dict(answer="Please, fill all fields!")
    assert response_password.json() == dict(answer="Incorrect data")


def test_logout():
    data_login_good = dict(email="tester@test.com", password="test_password")
    session.post(f'{base_url}/login', json=data_login_good, allow_redirects=True)

    response = session.post(f'{base_url}/logout')
    assert response.json(), dict(answer="Logout successful.")

    bad_logout = requests.post(f'{base_url}/logout')
    assert bad_logout.json(), "Unauthorized"
