from flask import request
from sqlalchemy.exc import PendingRollbackError, IntegrityError
from werkzeug.datastructures import ImmutableMultiDict

from ..database.forms.film_form import FilmForm, FilmEditForm
from ..database.models.film import Film


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
    """
    Function allows you to validate the correctness of the data for creating a new movie and create a new movie.
    :param movie_title:
    :param release_date:
    :param rating:
    :param user_id:
    :param data:
    :return:
    """
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
    """
    Function takes the data and passes it to the subsequent removal of the movie.
    :param method:
    :param users:
    :return:
    """
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


def edit_film(user, film_id):
    """
    Function allows you to edit the movie.
    :
    :param user:
    :param film_id:
    :return:
    """
    film = Film.query.filter_by(id=film_id).first()
    if not film:
        return 'Film not Found'
    if film.id_user != user.id and user.role.role_name != 'admin':
        return f'{film.id_user}{user.id}{user.role.role_name}'

    data = request.get_json()
    form_input = ImmutableMultiDict(data)
    if FilmEditForm(form_input).validate():
        film.id_director = data["id_director"] if data[
            "id_director"] else film.id_director if film.id_director else None
        film.description = data["description"] if data["description"] else film.description
        film.movie_title = data["movie_title"] if data["movie_title"] else film.movie_title
        film.poster = data["poster"] if data["poster"] else film.poster if film.poster else None
        film.rating = data["rating"] if data["rating"] else film.rating
        film.genre = data['genre'] if data["genre"] else film.genre if film.id_genre else None
        film.release_date = data['release_date'] if data["release_date"] else film.release_date

        film.update_from_db()
        return 'Movies have been successfully modified'
    return 'Incorrect data'


def film_view(film_id):
    """
    Function allows you to view all information about the movie.
    :
    :param film_id:
    :return:
    """
    film = Film.query.filter_by(id=film_id).first()
    if film:
        return {'Description': film.description if film.description else "Unknown",
                'Movie title': film.movie_title,
                'Poster': film.poster if film.poster else "Unknown",
                'Rating': film.rating,
                'Genre': film.id_genre if film.id_genre else "Unknown",
                'Release date': film.release_date,
                'Director': [film.director.last_name, film.director.first_name] if film.id_director else 'Unknown'}
    return "Film Not found"
