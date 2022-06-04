"""
Module that takes on the functionality of adding new users to the site,
 adding new films and deleting them.
"""

from flask import request, redirect
from flask_login import login_user
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.security import generate_password_hash, check_password_hash

from .database.forms.film_form import FilmForm, SearchForm
from .database.forms.user_form import RegistrationForm, LoginForm
from .database.models.film import Film
from .database.models.user import User
from .database.shemes.schema import FilmSchema
from .views import MovieView


def init_add_user():
    data = request.get_json(force=True)
    nickname: str = data["nickname"]
    last_name: str = data["last_name"]
    first_name: str = data["first_name"]
    email: str = data["email"]
    password: str = data["password"]
    password2: str = data["password2"]
    return add_user(nickname, last_name, first_name, email, password, password2, data)


def add_user(nickname: str, last_name: str, first_name: str, email: str, password: str, password2: str,
             data: dict) -> object:
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
            new_user: object = User(nickname=nickname, last_name=last_name, first_name=first_name, email=email,
                                    password=hash_pwd)
            new_user.save_to_db()
            return f"'{new_user.nickname}' created."
        except IntegrityError or PendingRollbackError:
            new_user.rollback()
            return f"user '{new_user.nickname}, {User.query.all()}' already exist."
    return 'Incorrect data'


def init_add_film(method: str, user_id: int):
    """
    Function is responsible for adding new movies to the site.
    :param method:
    :param user_id:
    :return:
    """
    if method == 'GET':
        movie_title: str = request.form.get('movie_title')
        release_date: int = request.form.get('release_date')
        rating: int = request.form.get('rating')
        # movie_title, release_date, rating, poster=None, description=None, id_director=None, id_user=None, id_genre=None
    if method == 'POST':
        data = request.get_json()
        movie_title: str = data["movie_title"]
        release_date: int = data["release_date"]
        rating: int = data["rating"]
    return add_film(movie_title, release_date, rating, user_id, data)


def add_film(movie_title: str, release_date: int, rating: int, user_id: int, data: dict) -> object:
    if not (movie_title or release_date or rating):
        return 'Please, fill all fields!',  # flash('Please, fill all fields!')
    form_input = ImmutableMultiDict(data)
    if FilmForm(form_input).validate():
        try:
            new_film = Film(movie_title=movie_title, release_date=release_date, rating=rating, id_user=user_id)
            new_film.save_to_db()
            return f"'{new_film.movie_title}' created."
        except IntegrityError or PendingRollbackError:
            new_film.rollback()
            return f"user '{new_film.movie_title}, {Film.query.all()}' already exist."
    return 'Incorrect data'


def init_del_film(method, users):
    if method == 'GET':
        movie_title = request.form.get('movie_title')  # movie_title = 'A team'
        return del_film(title=movie_title, user=users)

    if method == 'POST':
        data = request.get_json()
        movie_title: str = data["movie_title"]
        return del_film(title=movie_title, user=users)


def del_film(title: str, user: object):
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


def init_login_user():
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
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return f"Welcome back, '{user}'"
    return 'bad password.'  # flash('bad password')


def general_page_views(method: str, page: int):
    if method == "GET":
        filters: str = request.args.get("filters") if request.args.get("filter") else None
        sorted_methods: str = request.args.get("sorted_methods") if request.args.get("sorted_methods") else None
        genres: list = request.args.get("genres") if request.args.get("genres") else []
        paginate: int = request.args.get("paginate") if request.args.get("paginate") else 10

        if filters:
            return MovieView.sorted_films(page, filters, sorted_methods, genres, paginate)
        return MovieView.show_all_film(page, filters, genres, paginate)
    if method == "POST":
        data = request.get_json()
        filters: str = data["filters"] if data["filters"] else None
        sorted_methods: str = data["sorted_methods"] if data["sorted_methods"] else None
        genres: list = data["genres"] if data["genres"] else []
        paginate: int = data["paginate"] if data["paginate"] else 10

        if filters:
            return MovieView.sorted_films(page, filters, sorted_methods, genres, paginate)
        return MovieView.show_all_film(page, filters, genres, paginate)


def search_films(method, search_elem=None):
    if method == 'GET':
        data ={"search": search_elem}
        form_input = ImmutableMultiDict(data)
        if SearchForm(form_input).validate():
            film_schema = FilmSchema(many=True)
            return film_schema.dump(Film.query.filter(Film.movie_title.like(f'%{search_elem}%')).all())
        return 123
    if method == "POST":
        data = request.get_json()
        search = data["search"]
        form_input = ImmutableMultiDict(data)
        if SearchForm(form_input).validate():
            film_schema = FilmSchema(many=True)
            return film_schema.dump(Film.query.filter(Film.movie_title.like(f'%{search}%')).all())
