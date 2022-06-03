"""
Module is responsible for displaying on the main page.
"""
from .database.models.film import Film
from .database.shemes.schema import FilmSchema


class MovieView:
    """
    Class is responsible for displaying movies.
    """

    @staticmethod
    def show_all_film(page: int, filters: str, genres: list, paginate: int):
        """
        Function displays all films without sorting but with the possibility of filtering.
        :param page:
        :param paginate:
        :param filters:
        :param genres:
        :return:
        """
        films: list = Film.query.paginate(page, paginate, False).items

        if filters == "genre":
            films = Film.query.filter(Film.id_genre in genres)

        if filters == "date":
            films = Film.query.filter(Film.release_date).paginate(page, paginate, False).items

        if filters == "director":
            films = Film.query.filter(Film.id_director).paginate(page, paginate, False).items

        film_schema = FilmSchema(many=True)
        return film_schema.dump(films)

    @staticmethod
    def sorted_films(page: int, filters: str, sorted_method: str, genres: list, paginate: int):
        """
        Function works on different options for sorting movies.
        :param page:
        :param sorted_method:
        :param paginate:
        :param filters:
        :param genres:
        :return:
        """
        if sorted_method not in ['rating', 'date']:
            return 'Invalid sorted method.'

        films = Film.query.order_by(Film.rating.desc()).paginate(page, paginate, False).items \
            if sorted_method == 'rating' else \
            Film.query.order_by(Film.release_date.desc()).paginate(page, paginate, False).items

        if filters == "genre":
            films = Film.query.filter(Film.id_genre in genres) \
                .order_by(Film.rating.desc()).paginate(page, paginate, False).items \
                if sorted_method == 'rating' else \
                Film.query.filter(Film.id_genre in genres). \
                    order_by(Film.release_date.desc()).paginate(page, paginate, False).items

        if filters == "date":
            films = Film.query.filter(Film.release_date) \
                .order_by(Film.rating.desc()).paginate(page, paginate, False).items \
                if sorted_method == 'rating' else \
                Film.query.filter(Film.release_date). \
                    order_by(Film.release_date.desc()).paginate(page, paginate, False).items

        if filters == "director":
            films = Film.query.filter(Film.id_director). \
                order_by(Film.rating.desc()).paginate(page, paginate, False).items \
                if sorted_method == 'rating' else \
                Film.query.filter(Film.id_director). \
                    order_by(Film.release_date.desc()).paginate(page, paginate, False).items

        film_schema = FilmSchema(many=True)
        return film_schema.dump(films)
