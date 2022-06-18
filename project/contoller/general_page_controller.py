"""
Module in which the controller for the main page is implemented.
"""

from werkzeug.datastructures import ImmutableMultiDict

from .sub_contoller_gp import SubController
from ..database.db_repository.film_repository import AbstractFilmRepository
from ..database.forms.film_form import SearchForm


def search_films(search_elem: str, repository: AbstractFilmRepository) -> tuple[dict | None, int] | tuple[str, int]:
    """
    Function does the job of finding and returning a list of movies.
    :param repository:
    :
    :param search_elem:
    :return:
    """
    data = {"search": search_elem}
    form_input = ImmutableMultiDict(data)
    if SearchForm(form_input).validate():
        film = repository.search_film_by_name(search_elem)
        if film:
            return render_search_film(film, repository)
        return "Film Not found", 204
    return 'Error', 409


def render_search_film(film: list, repository: AbstractFilmRepository) -> tuple[dict | None, int]:
    """
    The function will perform auxiliary work for issuing a movie search.
    :param repository:
    :param film:
    :return:
    """
    if len(film) > 1:
        films = {i + 1: repository.return_film_view(film=film[i],
                                                    list_genre=repository.get_name_genre(film[i].id))
                 for i in range(len(film))}
    elif len(film) == 1:
        films = repository.return_film_view(film=film[0], list_genre=repository.get_name_genre(film[0].id))
    return films, 200


def general_page_views(data: dict, page: int, repository: AbstractFilmRepository) -> tuple[str, int] | tuple[
    dict | None, int]:
    """
    Function using a view displays movies on the main page.
    :param repository:
    :param data:
    :param page:
    :return:
    """
    sub_controller: SubController = SubController()

    sorted_methods: list = sub_controller.check_sorted_methods(sub_controller.del_duplicate(data["sorted_methods"]))
    genres: list = sub_controller.check_genre(data["genres"], repository)
    paginate: int = data["paginate"] if data["paginate"] != 0 else 10
    director_id: list = sub_controller.check_director_id(data["director_id"], repository)
    filters: dict = sub_controller.check_filter_method(sub_controller.del_duplicate(data["filters"])
                                                       , genres, director_id, data["min_date"], data["max_date"])

    command = sub_controller.create_command(sorted_methods, filters, repository)
    film = repository.start_command(command, page, paginate)

    if not film:
        return "Films Not found", 204
    return render_search_film(film, repository)
