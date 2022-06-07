"""
Module in which the controller for the main page is implemented.
"""
from werkzeug.datastructures import ImmutableMultiDict

from ..database.forms.film_form import SearchForm
from ..database.models.film import Film
from ..database.shemes.schema import FilmSchema
from ..views import MovieView


def search_films(search_elem: str = None):
    """
    Function does the job of finding and returning a list of movies.
    :
    :param search_elem:
    :return:
    """
    data = {"search": search_elem}
    form_input = ImmutableMultiDict(data)
    if SearchForm(form_input).validate():
        film_schema = FilmSchema(many=True)
        film = Film.query.filter(Film.movie_title.like(f'%{search_elem}%')).all()
        return film_schema.dump(film)
    return 'Error'


def general_page_views(data: dict, page: int):
    """
    Function using a view displays movies on the main page.
    :
    :param data:
    :param page:
    :return:
    """
    filters: str = data["filters"] if data["filters"] else None
    sorted_methods: str = data["sorted_methods"] if data["sorted_methods"] else None
    genres: list = data["genres"] if data["genres"] != 0 else None
    paginate: int = data["paginate"] if data["paginate"] != 0 else 10
    director_id: int = data["director_id"] if data["director_id"] != 0 else None
    min_date: int = data["min_date"] if data["min_date"] else None
    max_date: int = data["max_date"] if data["max_date"] else None

    if sorted_methods:
        return MovieView.sorted_films(page, filters, sorted_methods, genres,
                                      paginate, director_id, min_date, max_date)
    return MovieView.show_all_film(page, filters, genres, paginate,
                                   director_id, min_date, max_date)
