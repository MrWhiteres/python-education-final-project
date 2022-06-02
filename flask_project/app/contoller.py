"""
Module that takes on the functionality of adding new users to the site,
 adding new films and deleting them.
"""
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from werkzeug.security import generate_password_hash

from .database.models.film import Film
from .database.models.user import User


def add_user(nickname, last_name, first_name, email, password, password2):
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
    try:
        hash_pwd = generate_password_hash(password)
        new_user = User(nickname=nickname, last_name=last_name, first_name=first_name, email=email,
                        password=hash_pwd)
        new_user.save_to_db()
        return f"'{new_user.nickname}' created."
    except IntegrityError or PendingRollbackError:
        new_user.rollback()
        return f"user '{new_user.nickname}, {User.query.all()}' already exist."


def add_films(movie_title, release_date, rating, poster=None, description=None,
              id_director=None, id_user=None, id_genre=None):
    """
    Function is responsible for adding new movies to the site.
    :param movie_title:
    :param release_date:
    :param rating:
    :param poster:
    :param description:
    :param id_director:
    :param id_user:
    :param id_genre:
    :return:
    """
    if not (movie_title or release_date or rating):
        return 'Please, fill all fields!'  # flash('Please, fill all fields!')
    try:
        new_film = Film(movie_title=movie_title, release_date=release_date, rating=rating, id_user=id_user)
        new_film.save_to_db()
        return f"'{new_film.movie_title}' created."
    except IntegrityError or PendingRollbackError:
        new_film.rollback()
        return f"user '{new_film.movie_title}, {Film.query.all()}' already exist."


def del_film(title, user):
    """
    Function is responsible for removing movies from the site.
    :param title:
    :param user:
    :return:
    """
    if not (title or user):
        return 'Please, fill all fields!'  # flash('Please, fill all fields!')
    try:
        old_film = Film.query.filter(Film.movie_title == title).first()
        if old_film.id_user == user.id or user.role.role_name == 'admin':
            old_film.delete_from_db()
            return f"'{title}' delete."
        return f"You can`t delete this film '{title}'."
    except AttributeError:
        return f"Film '{title}' not found."
