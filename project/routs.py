"""
Module implements all the paths of the address bar in the flask application.
"""
from flask import jsonify, make_response
from flask_login import login_required, logout_user, current_user
from flask_restx import Resource

from .app import api
from .contoller.film_controller import film_view, init_add_film, init_del_film, edit_film
from .contoller.general_page_controller import general_page_views, search_films
from .contoller.user_controller import init_login_user, profile, init_add_user
from .database.db_repository.film_repository import FilmRepository
from .database.db_repository.user_repository import UserRepository
from .model_view import registration_user_model, login_user_model, film_model, del_film_model, general_page_model, \
    film_edit_model


@api.route("/")
@api.route("/<int:pk>")
@api.expect(general_page_model)
class GeneralPage(Resource):
    @staticmethod
    @api.doc(model=general_page_model)
    def post(pk=1):
        """
        Function using a view displays movies on the main page.
        :param filters [genre/date/director/""]:
        :param sorted_methods [rating/date/""]:
        :param genres [str]:
        :param paginate [default 10]:
        :param director_id [int]:
        if filters == date
        :param min_date [default=""(not min_date)] data type 'YYYY/MM/DD':
        and
        :param max_date [default=""(not max_date)] data type 'YYYY/MM/DD':
        :param pk:
        :return:
        """
        body, code = general_page_views(api.payload, pk, FilmRepository)
        return make_response(jsonify(Film=body), code)


@api.route("/film/<int:id_film>")
class FilmView(Resource):
    @staticmethod
    def get(id_film):
        """
            Film View Page.
            Route takes the id of the movies and checks it if there is a movie with this id if it exists,
            returns information about this movie if not,
            returns the answer that the movie is not in the database.

            :param id_film:
            :return:
        """
        body, code = film_view(id_film, FilmRepository)
        return make_response(jsonify(Film=body), code)


@api.route('/add_film')
@api.expect(film_model)
class AddFilm(Resource):

    @staticmethod
    @login_required
    @api.doc(model=film_model)
    def post():
        """
        Route to add new movies to the site.
        Function is responsible for adding new movies to the site.
        :param movie_title:
        :param release_date (data type 'YYYY/MM/DD'):
        :param rating:
        :param poster:
        :param description:
        :param genre:
        :param id_director:
        :return:
        """
        body, code = init_add_film(data=api.payload, user=current_user, repository=FilmRepository)
        return make_response(jsonify(answer=body), code)


@api.route('/del_films')
@api.expect(del_film_model)
class DelFilm(Resource):

    @staticmethod
    @login_required
    @api.doc(model=del_film_model)
    def post():
        """
        Route to remove movies from the site.
        :param movie_title:
        :return:
        """
        body, code = init_del_film(data=api.payload, users=current_user, repository=FilmRepository)
        return make_response(jsonify(answer=body), code)


@api.route('/login')
@api.expect(login_user_model)
class LoginUser(Resource):
    @staticmethod
    @api.doc(model=login_user_model)
    def post():
        """
        Route for user authorization on the site if it is in the database.
        :param email:
        :param password:
        :return:
        """
        body, code = init_login_user(api.payload, UserRepository)
        return make_response(jsonify(answer=body), code)


@api.route('/registration')
class Registration(Resource):
    @staticmethod
    @api.expect(registration_user_model)
    def post():
        """
        Route for registering new users on the site.

        :param nickname:
        :param last_name:
        :param first_name:
        :param email:
        :param password:
        :param password2:
        :return:
        """
        body, code = init_add_user(api.payload, UserRepository)
        return make_response(jsonify(answer=body), code)


@api.route('/logout')
class LogoutUser(Resource):

    @staticmethod
    @login_required
    def post():
        """
        Route to log out of user account.
        :return:
        """
        logout_user()
        return make_response(jsonify(answer="Logout successful."))


@api.route('/search/<search>')
class Search(Resource):
    @staticmethod
    def get(search):
        """
        Movie search route.
        The route is designed to work with a search for a complete or partial match of films.
        :param search:
        :return:
        """
        body, code = search_films(search, FilmRepository)
        return make_response(jsonify(answer=body), code)


@api.route('/profile/<int:profile_id>')
class Profile(Resource):

    @staticmethod
    @login_required
    def get(profile_id):
        """
        User profile route.
        Router adds the ability to allow the user to view information about their account.
        :param profile_id:
        :return:
        """
        body, code = profile(current_user, profile_id, UserRepository)
        return make_response(jsonify({'User Profile': body}), code)


@api.route("/edit/film/<string:film_title>")
@api.expect(film_edit_model)
class Edit(Resource):

    @staticmethod
    @login_required
    @api.doc(film_edit_model)
    def post(film_title):
        """
        Route fo edit films.
        Route takes a movie ID And if there is such a movie,
         it allows you to change the data about this movie
          with subsequent recording of changes in the database

        :param film_title:
        :param movie_title:
        :param release_date (data type 'YYYY/MM/DD'):
        :param rating:
        :param poster:
        :param description:
        :param genre:
        :param id_director:
        :return:
        """
        body, code = edit_film(api.payload, current_user, film_title, FilmRepository)
        return make_response(jsonify(Film=body), code)
