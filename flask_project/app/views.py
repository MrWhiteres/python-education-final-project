from .database.models.film import Film, FilmSchema


class MovieView:
    @staticmethod
    def show_all_film(page, paginate=10, filter=None):
        films = Film.query.paginate(page, paginate, False).items
        film_schema = FilmSchema(many=True)
        return film_schema.dump(films)

    @staticmethod
    def sorted_rating(page, paginate=10, filter=None):
        films = Film.query.order_by(Film.rating.desc()).paginate(page, paginate, False).items
        film_schema = FilmSchema(many=True)
        return film_schema.dump(films).data

    @staticmethod
    def sorted_release_date(page, paginate=10, filter=None):
        films = Film.query.order_by(Film.release_date.desc()).paginate(page, paginate, False).items
        film_schema = FilmSchema(many=True)
        return film_schema.dump(films).data
