"""
Module in which the controller for the main page is implemented.
"""
from flask import request
from werkzeug.datastructures import ImmutableMultiDict

from ..database.forms.film_form import SearchForm
from ..database.models.film import Film
from ..database.shemes.schema import FilmSchema
from ..views import MovieView


def search_films(method, search_elem=None):
    """
    Function does the job of finding and returning a list of movies.
    :
    :param method:
    :param search_elem:
    :return:
    """
    if method == 'GET':
        data = {"search": search_elem}
        form_input = ImmutableMultiDict(data)
        if SearchForm(form_input).validate():
            film_schema = FilmSchema(many=True)
            film = Film.query.filter(Film.movie_title.like(f'%{search_elem}%')).all()
            return film_schema.dump(film)
    if method == "POST":
        data = request.get_json()
        search = data["search"]
        form_input = ImmutableMultiDict(data)
        if SearchForm(form_input).validate():
            film_schema = FilmSchema(many=True)
            return film_schema.dump(Film.query.filter(Film.movie_title.like(f'%{search}%')).all())
    return 'Error'


def general_page_views(method: str, page: int):
    """
    Function using a view displays movies on the main page.
    :
    :param method:
    :param page:
    :return:
    """
    if method == "GET":
        filters: str = request.args.get("filters") if request.args.get("filter") else None
        sorted_methods: str = request.args.get("sorted_methods") if request.args.get("sorted_methods") else None
        genres: list = request.args.get("genres") if request.args.get("genres") else None
        paginate: int = request.args.get("paginate") if request.args.get("paginate") else 10
        director_id: int = request.args.get("director_id") if request.args.get("director_id") else None
        min_date: int = request.args.get("min_date") if request.args.get("min_date") else None
        max_date: int = request.args.get("max_date") if request.args.get("max_date") else None
        if sorted_methods:
            return MovieView.sorted_films(page, filters, sorted_methods, genres,
                                          paginate, director_id, min_date, max_date)
        return MovieView.show_all_film(page, filters, genres, paginate,
                                       director_id, min_date, max_date)
    if method == "POST":
        data = request.get_json()
        filters: str = data["filters"] if data["filters"] else None
        sorted_methods: str = data["sorted_methods"] if data["sorted_methods"] else None
        genres: list = data["genres"] if data["genres"] else None
        paginate: int = data["paginate"] if data["paginate"] else 10
        director_id: int = data["director_id"] if data["director_id"] else None
        min_date: int = data["min_date"] if data["min_date"] else None
        max_date: int = data["max_date"] if data["max_date"] else None

        if sorted_methods:
            return MovieView.sorted_films(page, filters, sorted_methods, genres,
                                          paginate, director_id, min_date, max_date)
        return MovieView.show_all_film(page, filters, genres, paginate,
                                       director_id, min_date, max_date)
