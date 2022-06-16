"""
Module is an auxiliary tool in working with the controller main page.
"""
from datetime import date

from ..database.db_repository.film_repository import AbstractFilmRepository


class SubController:
    @staticmethod
    def create_command(sorted_methods: list, filters: dict, repository: AbstractFilmRepository) -> str:
        """
        Method creates a command line to filter the sorting of movies.
        :param repository:
        :param sorted_methods:
        :param filters:
        :return:
        """
        command = ""
        if sorted_methods:
            command = repository.add_sorted_in_command(command, sorted_methods)
        if filters:
            command = repository.add_filter_in_command(command, filters)
        return command

    @staticmethod
    def del_duplicate(list_set_list: list) -> list:
        """
        Method removes duplicates from the list it accepts.
        :param list_set_list:
        :return:
        """
        return list(set(list_set_list))

    def check_director_id(self, list_director, repository: AbstractFilmRepository) -> list or None:
        """
        Method searches for a movie director by his ID.
        :param repository:
        :param list_director:
        :return:
        """
        if len(list_director) > 0:
            return self.sub_check_director_id(list_director, repository)
        return None

    def sub_check_director_id(self, list_id, repository: AbstractFilmRepository) -> list:
        """
        Managing part in the search for a film director.
        :param repository:
        :param list_id:
        :return:
        """
        return self.del_duplicate([repository.get_director(i) for i in list_id])

    @staticmethod
    def check_genre(list_genre: list, repository: AbstractFilmRepository) -> list or None:
        """
        Method checks movie genre.
        :param repository:
        :param list_genre:
        :return:
        """
        if len(list_genre) > 0:
            return list(repository.get_genre(list_genre))
        return None

    def check_filter_method(self, list_methods: list, list_genre: list,
                            list_director: list, min_date: date, max_date: date) -> dict or None:
        """
        Method executes initializes the role in creating a dictionary for further processing of movie data.
        :param list_methods:
        :param list_genre:
        :param list_director:
        :param min_date:
        :param max_date:
        :return:
        """
        if 1 <= len(list_methods) <= 3:
            return self.sub_check_filter_method(len(list_methods), list_methods, list_genre, list_director, min_date,
                                                max_date)
        return None

    @staticmethod
    def sub_check_filter_method(len_list: int, list_method: dict, list_genre: list,
                                list_director: list, min_date: date, max_date: date) -> dict or None:
        """
        Method is the executing part of the formation of the dictionary.
        :param len_list:
        :param list_method:
        :param list_genre:
        :param list_director:
        :param min_date:
        :param max_date:
        :return:
        """
        count = 0
        result = dict()
        for i in list_method:
            if i in ("genre", "date", "director"):
                if i == "genre":
                    result["genre"] = list_genre
                if i == "date":
                    result["date"] = [min_date, max_date]
                if i == "director":
                    result["director"] = list_director
                count += 1
        if count == len_list:
            return result
        return None

    @staticmethod
    def check_sorted_methods(list_methods: list) -> list or None:
        """
        Method check sort methods.
        :param list_methods:
        :return:
        """
        if len(list_methods) == 1 and list_methods[0] in ('rating', "date"):
            return list_methods
        if len(list_methods) == 2 and "rating" in list_methods and "date" in list_methods:
            return list_methods
        return None
