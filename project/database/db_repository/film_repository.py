"""
Module for working with a table in the film database.
"""
from sqlalchemy import update, or_

from . import AbstractRepository, ABC, abstractmethod
from .. import db
from ..models.director import Director
from ..models.film import Film
from ..models.genre import Genre
from ..models.genre_film import genre_film


class AbstractFilmRepository(ABC):
    """
    Abstract Film Repository.
    """
    @abstractmethod
    def search_film_by_name(self, search_elem):
        """ABC method for FilmRepository.search_film_by_name"""

    @abstractmethod
    def return_film_view(self, film, list_genre):
        """ABC method for FilmRepository.return_film_view"""

    @abstractmethod
    def get_name_genre(self, id):
        """ABC method for FilmRepository.get_name_genre"""

    @abstractmethod
    def start_command(self, command, page, paginate):
        """ABC method for FilmRepository.start_command"""

    @abstractmethod
    def get_director(self, param):
        """ABC method for FilmRepository.get_director"""

    @abstractmethod
    def get_genre(self, genre_list):
        """ABC method for FilmRepository.get_genre"""

    @abstractmethod
    def add_new_film(self, param):
        """ABC method for FilmRepository.add_new_film"""

    def add_genre(self, film_id, genre_list):
        """ABC method for FilmRepository.add_genre"""

    @abstractmethod
    def get_film_by_title(self, param):
        """ABC method for FilmRepository.get_film_by_title"""

    @abstractmethod
    def del_film(self, old_film):
        """ABC method for FilmRepository.del_film"""

    @abstractmethod
    def edit_film(self, title, data):
        """ABC method for FilmRepository.edit_film"""

    @abstractmethod
    def get_film_by_id(self, film_id):
        """ABC method for FilmRepository.get_film_by_id"""

    @abstractmethod
    def add_sorted_in_command(self, command, sorted_methods):
        """ABC method for FilmRepository.add_sorted_in_command"""

    @abstractmethod
    def add_filter_in_command(self, command, filters):
        """ABC method for FilmRepository.add_filter_in_command"""


class FilmRepository(AbstractRepository, AbstractFilmRepository):
    """
    Film Repository.
    """

    @staticmethod
    def get_genre(genre_list: list) -> set:
        """The function returns a list of records from the database if they are there."""
        genre_id_set = set()
        for i in genre_list:
            genre = Genre.query.filter_by(genre_name=i.lower()).first()
            if not genre:
                genre = Genre.query.filter_by(genre_name='unknown').first()
            genre_id_set.add(genre)
        return genre_id_set

    @staticmethod
    def get_director(id_director: int) -> int:
        """
        Method returns the director if it exists.
        :param id_director:
        :return:
        """
        director = Director.query.filter_by(id=id_director).first()
        if not director:
            director = Director.query.filter_by(last_name='unknown', first_name='unknown').first()
        return director.id

    @staticmethod
    def add_genre(film_id: int, genre_list: set):
        """The function adds genres to the movie"""
        for i in genre_list:
            answer = genre_film.insert().values(film_id=film_id, genre_id=i.id)
            db.session.execute(answer)
            db.session.commit()

    @staticmethod
    def add_new_film(movie_title: str, release_date: int, rating: int, poster: str, description: str,
                     id_director: int, user_id: int) -> Film:
        """
        Method adds new movie to database table.
        :param movie_title:
        :param release_date:
        :param rating:
        :param poster:
        :param description:
        :param id_director:
        :param user_id:
        :return:
        """
        film = Film(movie_title=movie_title, release_date=release_date, rating=rating, poster=poster,
                    description=description, id_director=id_director, id_user=user_id)
        film.save_to_db()
        return film

    @staticmethod
    def get_film_by_title(title: str) -> list[Film]:
        """
        Method returns the movie by its name.
        :param title:
        :return:
        """
        return Film.query.filter(Film.movie_title == title).first()

    @staticmethod
    def del_film(film: Film):
        """
        Method performs the function of removing the movie.
        :param film:
        :return:
        """
        film.delete_from_db()

    @staticmethod
    def edit_film(title: str, data: dict):
        """
        Method allows you to change the data of the movie.
        :param title:
        :param data:
        :return:
        """
        stmt = update(Film).where(Film.movie_title == title).values(**data)
        db.session.execute(stmt)
        db.session.commit()

    @staticmethod
    def get_film_by_id(film_id) -> list[Film]:
        """
        Method returns the movie by its id.
        :param film_id:
        :return:
        """
        return Film.query.filter_by(id=film_id).first()

    @staticmethod
    def get_name_genre(film_id: int) -> str:
        """The method returns a string with movie genres."""
        film_genre = db.session.query(genre_film).filter_by(film_id=film_id).all()
        genre_list = set()
        for i in film_genre:
            genre = Genre.query.filter_by(id=i.genre_id).first()
            genre_list.add(genre.genre_name)
        if len(genre_list) == 1 and 'unknown' in genre_list:
            genre_list = 'Unknown'
        elif len(genre_list) == 1 and "unknown" not in genre_list:
            genre_list = "".join(genre_list)
        elif len(genre_list) > 1:
            genre_list.discard('unknown')
            genre_list = ', '.join(list(genre_list))
        return genre_list

    @staticmethod
    def search_film_by_name(title) -> list[Film]:
        """
        Method allows you to find movies by partial matches in their names.
        :param title:
        :return:
        """
        return Film.query.filter(Film.movie_title.like(f'%{title}%')).all()

    @staticmethod
    def return_film_view(film: object, list_genre: str) -> dict:
        """
        Method renders a visualization of movie date.
        :param film:
        :param list_genre:
        :return:
        """
        return {'Movie title': film.movie_title,
                'Description': film.description,
                 'Poster': film.poster,
                 'Rating': film.rating,
                 'Genre': list_genre,
                 'Release date': film.release_date,
                 'Director': " ".join([film.director.last_name, film.director.first_name])
                 if film.director.first_name != "unknown"
                 else 'Unknown'}

    @staticmethod
    def add_filter_in_command(command: str, filters: dict) -> str:
        """
        Method fills the command with data about filtering.
        :param command:
        :param filters:
        :return:
        """
        if "genre" in filters and filters["genre"]:
            genre_list = []
            for i in filters["genre"]:
                genre_list.append(f"Genre.id == {i.id}")
            command += f".filter(or_({','.join(genre_list)}))"

        if "date" in filters and filters["date"]:
            command += f".filter(Film.release_date.between('{filters['date'][0]}', '{filters['date'][1]}'))"

        if "director" in filters and filters["director"]:
            director_list = []
            for i in filters["director"]:
                director_list.append(f'Film.id_director == {i}')
            command += f".filter(or_({','.join(director_list)}))"

        return command

    @staticmethod
    def add_sorted_in_command(command: str, sorted_list: list) -> str:
        """
        Method fills the command with data about sorting method.
        :param command:
        :param sorted_list:
        :return:
        """
        if len(sorted_list) == 1:
            if 'rating' in sorted_list:
                command += ".order_by(Film.rating.desc())"
            if 'date' in sorted_list:
                command += ".order_by(Film.release_date.desc())"
        if len(sorted_list) == 2 and ('date' in sorted_list and 'rating' in sorted_list):
            command += '.order_by(Film.release_date.desc()).order_by(Film.rating.desc())'
        return command

    @staticmethod
    def start_command(command: str, page: int, paginate: int) -> list[Film]:
        """
        The method using the 'eval' command runs the command.
        :param command:
        :param page:
        :param paginate:
        :return:
        """
        command += f".paginate({page}, {paginate}, {False}).items"
        command = "Film.query" + command
        return eval(command)
