from sqlalchemy.exc import PendingRollbackError, IntegrityError
from werkzeug.datastructures import ImmutableMultiDict

from ..database.db_repository.film_repository import AbstractFilmRepository
from ..database.forms.film_form import FilmForm, FilmEditForm
from ..database.models.user import User
from ..logger import logger


def init_add_film(data: dict, user: User, repository: AbstractFilmRepository) -> tuple[str, int]:
    """
    Function is responsible for adding new movies to the site.
    :param repository:
    :param user:
    :param data:
    :return:
    """
    genre: list = data['genre']
    del data["genre"]
    data['id_director'] = repository.get_director(data['id_director'])
    data['user_id'] = user.id

    if (data["movie_title"] or data["release_date"] or data["rating"] or data['poster'] or data['description'] or data[
        'id_director']) and len(genre) >= 1:
        form_input = ImmutableMultiDict(data)
        if FilmForm(form_input).validate():
            try:
                genre_set = repository.get_genre(genre_list=genre)
                new_film = repository.add_new_film(**data)
                logger.info(f"User - '{user.nickname}', add new film to db - '{new_film.movie_title}'")
                repository.add_genre(film_id=new_film.id, genre_list=genre_set)
                return f"'{new_film.movie_title}' created.", 201

            except IntegrityError or PendingRollbackError:
                logger.error(f"Add new film failed, film already exists.")
                return "Film already exist.", 409

        logger.error("Incorrect data was entered when adding a new movie.")
        return 'Incorrect data', 409
    return 'Please, fill all fields!', 409


def init_del_film(data: dict, users: User, repository: AbstractFilmRepository) -> tuple[str, int]:
    """
    Function takes the data and passes it to the subsequent removal of the movie.
    :param repository:
    :param data:
    :param users:
    :return:
    """
    data["users"] = users
    if not data["movie_title"]:
        return 'Please, fill all fields!', 409
    try:
        old_film = repository.get_film_by_title(data["movie_title"])
        if old_film.id_user == data["users"].id or data["users"].role.role_name == 'admin':
            repository.del_film(old_film)
            logger.info("Del_Film", f"User - '{data['users'].nickname}', del film - '{data['movie_title']}'")
            return f"'{data['movie_title']}' delete.", 200

        logger.error(f"User - '{data['users'].nickname}', try del film - '{data['movie_title']}'")
        return f"You can`t delete this film '{data['movie_title']}'.", 403

    except AttributeError:

        logger.error(f"User - '{data['users'].nickname}', try del film - '{data['movie_title']}', not found")
        return f"Film '{data['movie_title']}' not found.", 204


def edit_film(data: dict, user: User, film_title: str, repository: AbstractFilmRepository) -> tuple:
    """
    Function allows you to edit the movie.
    :param repository:
    :param film_title:
    :param data:
    :param user:
    :return:
    """
    film = repository.get_film_by_title(film_title)
    if not film:
        return "Film Not found", 204

    if film.id_user != user.id and user.role.role_name != 'admin':
        return f'You cannot edit this film.', 403

    film_title = film.movie_title
    form_input = ImmutableMultiDict(data)

    if FilmEditForm(form_input).validate():
        repository.edit_film(title=film_title, data=data)
        logger.info(f"User - '{user.nickname}', changed movie info '<{film_title}, film id {film.id}>'.")
        return 'Movies have been successfully modified', 200

    logger.error(f"User - '{user.nickname}', try changed movie info '<{film_title}, incorrect data entered.")
    return 'Incorrect data', 409


def film_view(film_id: int, repository: AbstractFilmRepository) -> tuple:
    """
    Function allows you to view all information about the movie.
    :param repository:
    :
    :param film_id:
    :return:
    """
    film = repository.get_film_by_id(film_id=film_id)
    if film:
        list_genre = repository.get_name_genre(film.id)
        return repository.return_film_view(film=film, list_genre=list_genre), 200
    return "Film Not found", 204
