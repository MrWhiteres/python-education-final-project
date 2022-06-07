from sqlalchemy.exc import PendingRollbackError, IntegrityError
from werkzeug.datastructures import ImmutableMultiDict

from ..database.forms.film_form import FilmForm, FilmEditForm
from ..database.models.film import Film
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
    poster: str = data['poster']
    description: str = data['description']
    genre: int = data['genre']
    id_director: int = data['id_director']
    return add_film(movie_title, release_date, rating, poster, description, genre, id_director, user, data)


def add_film(movie_title: str, release_date: int, rating: int, poster: str, description: str, genre: int,
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
        :param user_id:
        :param data:
        :return:
    """
    if not (movie_title or release_date or rating):
        return 'Please, fill all fields!'
    form_input = ImmutableMultiDict(data)
    if FilmForm(form_input).validate():
        try:
            poster = poster if poster else None
            description = description if description else None
            genre = genre if genre != 0 else []
            id_director = id_director if id_director != 0 else None
            new_film = Film(movie_title=movie_title, release_date=release_date, rating=rating, poster=poster,
                            description=description, id_genre=genre, id_director=id_director, id_user=user.id)
            new_film.save_to_db()
            logger.info(f"User - '{user.nickname}', add new film to db - '{new_film.movie_title}'")
            return f"'{new_film.movie_title}' created."

        except IntegrityError or PendingRollbackError:
            logger.error(f"Add new film '{new_film.movie_title}' failed, film already exists.")
            new_film.rollback()
            return f"user '{new_film.movie_title}, {Film.query.all()}' already exist."

    logger.error("Incorrect data was entered when adding a new movie.")
    return 'Incorrect data'


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


def edit_film(data: dict, user: object, film_id: int):
    """
    Function allows you to edit the movie.
    :param data:
    :param user:
    :param film_id:
    :return:
    """
    film = Film.query.filter_by(id=film_id).first()
    if not film:
        return 'Film not Found'
    if film.id_user != user.id and user.role.role_name != 'admin':
        return f'You cannot edit this film: {film.id_user}{user.id}{user.role.role_name}'
    film_title = film.movie_title
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
