"""
Module is a controller initializer for operations with users.
"""
from flask import request, redirect
from flask_login import login_user
from sqlalchemy.exc import PendingRollbackError, IntegrityError
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from ..database.forms.user_form import LoginForm
from ..database.forms.user_form import RegistrationForm
from ..database.models.user import User


def profile_user(method, users, profile_id=None):
    """
    Function to return this user data.
    :param method:
    :param users:
    :param profile_id:
    :return:
    """
    if method == "POST":
        data = request.get_json()
        profile_id = data['profile_id']
        return profiles(users, profile_id)
    return profiles(users, profile_id)


def profiles(users, profile_id):
    """
    Function checks the user id and his role then returns the data.
    :param users:
    :param profile_id:
    :return:
    """
    if users.id == profile_id or users.role.role_name == 'admin':
        user = User.query.filter_by(id=profile_id).first()
        return {'Nickname': user.nickname, 'Last Name': user.last_name,
                'First Name': user.first_name, 'Email': user.email, 'Role': user.role.role_name}
    return "There's nothing here."


def init_add_user():
    """
    Function collects information and then passes it to create a new user.
    :return:
    """
    data = request.get_json(force=True)
    nickname: str = data["nickname"]
    last_name: str = data["last_name"]
    first_name: str = data["first_name"]
    email: str = data["email"]
    password: str = data["password"]
    password2: str = data["password2"]
    return add_user(nickname, last_name, first_name, email, password, password2, data)


def add_user(nickname: str, last_name: str, first_name: str,
             email: str, password: str, password2: str, data: dict) -> object:
    """
    Function is responsible for adding and checking new users.
    :param nickname:
    :param last_name:
    :param first_name:
    :param email:
    :param password:
    :param password2:
    :return:
    """
    if not (nickname or last_name or first_name or email or password or password2):
        return 'Please, fill all fields!'  # flash('Please, fill all fields!')
    if password != password2:
        return 'Passwords are not equal!'  # flash('Passwords are not equal!')
    form_input = ImmutableMultiDict(data)
    if RegistrationForm(form_input).validate():
        try:
            hash_pwd = generate_password_hash(password)
            new_user: object = User(nickname=nickname, last_name=last_name,
                                    first_name=first_name, email=email, password=hash_pwd)
            new_user.save_to_db()
            return f"'{new_user.nickname}' created."
        except (IntegrityError, PendingRollbackError):
            new_user.rollback()
            return f"user '{new_user.nickname}, {User.query.all()}' already exist."
    return 'Incorrect data'


def init_login_user():
    """
    Function collects user information and then passes i to check if such a user is in the database.
    :return:
    """
    data = request.get_json()
    email: str = data["email"]
    password: str = data["password"]
    form_input = ImmutableMultiDict(data)
    if email and password and LoginForm(form_input).validate():
        next_page = request.args.get("next")
        if not next_page:
            return login_users(email, password)
        login_users(email, password)
        return redirect(next_page)

    return 'Please, fill all fields!'


def login_users(email: str, password: str):
    """
    Function allows the user to log in to the site when entering the correct data.
    :param email:
    :param password:
    :return:
    """
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return f"Welcome back, '{user}'"
    return 'bad password.'  # flash('bad password')
