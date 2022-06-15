from sqlalchemy import update
from sqlalchemy.exc import PendingRollbackError, IntegrityError
from werkzeug.datastructures import ImmutableMultiDict

from ..database import db
from ..database.forms.film_form import FilmForm, FilmEditForm
from ..database.models.film import Film
from ..database.models.genre import Genre
from ..database.models.genre_film import genre_film
from ..logger import logger


def init_add_film(data: dict, user: object):
    """
    Function is responsible for adding new movies to the site.
    :param user:
    :param data:
    :return:
    """
    movie_title: str = data["movie_title"]
    release_date: int = data["release_date"]
    rating: int = data["rating"]
    poster: str = data['poster'] if data['poster'] else None
    description: str = data['description'] if data['description'] else None
    genre: list = data['genre'] if data['genre'] else None
    id_director: int = data['id_director'] if data['id_director'] else None
    return add_film(movie_title, release_date, rating, poster, description, genre, id_director, user, data)


def add_film(movie_title: str, release_date: int, rating: int, poster: str, description: str, genre: list,
             id_director: int, user: object, data: dict) -> object:
    """
        Function allows you to validate the correctness of the data for creating a new movie and create a new movie.
        :param user:
        :param id_director:
        :param genre:
        :param description:
        :param poster:
        :param movie_title:
        :param release_date:
        :param rating:
        :param data:
        :return:
    """
    if (movie_title or release_date or rating or poster or description or id_director) and len(genre) >= 1:
        form_input = ImmutableMultiDict(data)
        if FilmForm(form_input).validate():
            try:
                genre_set = get_genre(genre_list=genre)
                new_film = Film(movie_title=movie_title, release_date=release_date, rating=rating, poster=poster,
                                description=description, id_director=id_director, id_user=user.id)
                new_film.save_to_db()
                logger.info(f"User - '{user.nickname}', add new film to db - '{new_film.movie_title}'")
                add_genre(film_id=new_film.id, genre_list=genre_set)
                return f"'{new_film.movie_title}' created."

            except IntegrityError or PendingRollbackError:
                logger.error(f"Add new film '{new_film.movie_title}' failed, film already exists.")
                new_film.rollback()
                return f"Film already exist."

        logger.error("Incorrect data was entered when adding a new movie.")
        return 'Incorrect data'
    return 'Please, fill all fields!'


def get_genre(genre_list: list) -> set:
    """The function returns a list of records from the database if they are there."""
    genre_id_set = set()
    for i in genre_list:
        genre = Genre.query.filter_by(genre_name=i).first()
        if genre:
            genre_id_set.add(genre)
        else:
            genre = Genre.query.filter_by(genre_name='unknown').first()
            genre_id_set.add(genre)
    return genre_id_set


def add_genre(film_id: int, genre_list: set):
    """The function adds genres to the movie"""
    for i in genre_list:
        answer = genre_film.insert().values(film_id=film_id, genre_id=i.id)
        db.session.execute(answer)
        db.session.commit()


def init_del_film(data: dict, users: object):
    """
    Function takes the data and passes it to the subsequent removal of the movie.
    :param data:
    :param users:
    :return:
    """
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
            logger.info("Del_Film", f"User - '{user.nickname}', del film - '{title}'")
            return f"'{title}' delete."

        logger.error(f"User - '{user.nickname}', try del film - '{title}'")
        return f"You can`t delete this film '{title}'."

    except AttributeError:

        logger.error(f"User - '{user.nickname}', try del film - '{title}', not found")
        return f"Film '{title}' not found."


def edit_film(data: dict, user: object, film_title: str):
    """
    Function allows you to edit the movie.
    :param data:
    :param user:
    :param film_id:
    :return:
    """
    film = Film.query.filter_by(movie_title=film_title).first()
    if not film:
        return 'Film not Found'
    if film.id_user != user.id and user.role.role_name != 'admin':
        return f'You cannot edit this film.'
    film_title = film.movie_title
    form_input = ImmutableMultiDict(data)
    if FilmEditForm(form_input).validate():
        stmt = update(Film).where(Film.movie_title == film_title).values(**data)
        db.session.execute(stmt)
        db.session.commit()
        logger.info(f"User - '{user.nickname}', changed movie info '<{film_title}, film id {film.id}>'.")
        return 'Movies have been successfully modified'

    logger.error(f"User - '{user.nickname}', try changed movie info '<{film_title}, incorrect data entered.")
    return 'Incorrect data'


def film_view(film_id: int):
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
