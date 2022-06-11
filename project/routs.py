"""
Module implements all the paths of the address bar in the flask application.
"""
from flask import jsonify
from flask_login import login_required, logout_user, current_user
from flask_restx import Resource

from .app import api
from .contoller.film_controller import film_view, init_add_film, init_del_film, edit_film
from .contoller.general_page_controller import general_page_views, search_films
from .contoller.user_controller import init_login_user, profile, init_add_user
from .model_view import registration_user_model, login_user_model, film_model, del_film_model, general_page_model


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
        :param genres [default=0(not genres)]:
        :param paginate [default 10]:
        :param director_id [default=0(not director)]:
        if filters == date
        :param min_date [default=""(not min_date)] data type 'YYYY/MM/DD':
        and
        :param max_date [default=""(not max_date)] data type 'YYYY/MM/DD':
        :param pk:
        :return:
        """
        return jsonify(Film=general_page_views(api.payload, pk))


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
        return jsonify(Film=film_view(id_film))


@login_required
@api.route('/add_film')
@api.expect(film_model)
class AddFilm(Resource):
    @staticmethod
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
        return jsonify(answer=init_add_film(data=api.payload, user=current_user))


@login_required
@api.route('/del_films')
@api.expect(del_film_model)
class DelFilm(Resource):
    @staticmethod
    @api.doc(model=del_film_model)
    def post():
        """
        Route to remove movies from the site.

        :param movie_title:
        :return:
        """
        return jsonify(answer=init_del_film(api.payload, current_user))


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
        return jsonify(answer=init_login_user(api.payload))


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
        return jsonify(answer=init_add_user(api.payload))


@login_required
@api.route('/logout')
class LogoutUser(Resource):
    user: str = current_user.nickname if current_user else 'Unknown'

    def get(self):
        """
        Route to log out of user account.
        :return:
        """
        logout_user()
        return jsonify(answer=f"Come back, {self.user}")

    def post(self):
        """
        Route to log out of user account.
        :return:
        """
        logout_user()
        return jsonify(answer=f"Come back, {self.user}")


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
        return jsonify(answer=search_films(search))


@login_required
@api.route('/profile/<int:profile_id>')
class Profile(Resource):
    @staticmethod
    def get(profile_id):
        """
        User profile route.
        Router adds the ability to allow the user to view information about their account.
        :param profile_id:
        :return:
        """
        return jsonify({'User Profile': profile(current_user, profile_id)})


@login_required
@api.route("/edit/film/<int:film_id>")
@api.expect(film_model)
class Edit(Resource):
    @staticmethod
    @api.doc(film_model)
    def post(film_id):
        """
        Route fo edit films.
        Route takes a movie ID And if there is such a movie,
         it allows you to change the data about this movie
          with subsequent recording of changes in the database

        :param film_id:
        :param movie_title:
        :param release_date (data type 'YYYY/MM/DD'):
        :param rating:
        :param poster:
        :param description:
        :param genre:
        :param id_director:
        :return:
        """
        return jsonify(Film=edit_film(current_user, film_id))

# @project.after_request
# class RedirectToSignin(Resource):
#     """
#     If the user tries to go to an address that is available only to registered users, this method will intercept him
#     and redirect him to a page with the possibility of authorization after the user is successfully authorized,
#     he is redirected to the page where he was.
#     :param response:
#     :return:
#     """
#     @staticmethod
#     def get(response):
#         if response.status_code == 401:
#             return redirect(url_for("login") + '?next=' + request.url)
#         return response
