"""
Module is responsible for displaying on the main page.
"""
from datetime import datetime

from .database.models.film import Film
from .database.models.genre import Genre
from .database.shemes.schema import FilmSchema


class MovieView:
    """
    Class is responsible for displaying movies.
    """

    @staticmethod
    def show_all_film(page: int, filters: str, genres: str, paginate: int,
                      director_id: int, min_date: datetime, max_date: datetime):
        """
        Function displays all films without sorting but with the possibility of filtering.
        :param director_id:
        :param min_date:
        :param max_date:
        :param page:
        :param paginate:
        :param filters:
        :param genres:
        :return:
        """
        films: list = Film.query.paginate(page, paginate, False).items
        # film = Film.query.order_by(Film.rating.desc())
        if filters == "genre":
            films = Film.query.filter(Film.id_genre).filter(Genre.genre_name == genres). \
                paginate(page, paginate, False).items

        if filters == "date":
            films = Film.query.filter(Film.release_date >= min_date) \
                .filter(Film.release_date <= max_date).paginate(page, paginate, False).items

        if filters == "director":
            films = Film.query.filter(Film.id_director == director_id) \
                .paginate(page, paginate, False).items

        film_schema = FilmSchema(many=True)
        return film_schema.dump(films)

    @staticmethod
    def sorted_films(page: int, filters: str, sorted_method: str,
                     genres: list, paginate: int, director_id: int,
                     min_date: datetime, max_date: datetime):
        """
        Function works on different options for sorting movies.
        :param min_date:
        :param max_date:
        :param director_id:
        :param page:
        :param sorted_method:
        :param paginate:
        :param filters:
        :param genres:
        :return:
        """
        if sorted_method and sorted_method not in ['rating', 'date']:
            return 'Invalid sorted method.'

        films = Film.query.order_by(Film.rating.desc()).paginate(page, paginate, False).items \
            if sorted_method == 'rating' else \
            Film.query.order_by(Film.release_date.desc()).paginate(page, paginate, False).items

        if filters == "genre":
            films = Film.query.filter(Film.id_genre).filter(Genre.genre_name == genres) \
                .order_by(Film.rating.desc()) \
                .paginate(page, paginate, False).items \
                if sorted_method == 'rating' else \
                Film.query.filter(Film.id_genre)\
                    .filter(Genre.genre_name == genres) \
                    .order_by(Film.release_date.desc()) \
                    .paginate(page, paginate, False).items

        if filters == "date":
            films = Film.query.filter(Film.release_date >= min_date). \
                filter(Film.release_date <= max_date).order_by(Film.rating.desc()) \
                .paginate(page, paginate, False).items \
                if sorted_method == 'rating' else \
                Film.query.filter(Film.release_date >= min_date) \
                    .filter(Film.release_date <= max_date)\
                    .order_by(Film.release_date.desc()) \
                    .paginate(page, paginate, False).items

        if filters == "director":
            films = Film.query.filter(Film.id_director == director_id). \
                order_by(Film.rating.desc()).paginate(page, paginate, False).items \
                if sorted_method == 'rating' else \
                Film.query.filter(Film.id_director == director_id) \
                    .order_by(Film.release_date.desc()) \
                    .paginate(page, paginate, False).items

        film_schema = FilmSchema(many=True)
        return film_schema.dump(films)
