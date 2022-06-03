"""
Module implements all the paths of the address bar in the flask application.
"""
from flask import jsonify, request, redirect, url_for
from flask_login import login_required, logout_user, login_user, current_user
from flask_paginate import get_page_parameter
from werkzeug.security import check_password_hash

from .app import app
from .contoller import add_user, add_films, del_film
from .database.models.user import User
from .views import MovieView


@app.route("/", methods=["GET", "POST"])
@app.route("/<int:page>", methods=["GET", "POST"])
def general_page(pk=1):
    search = None
    page = request.args.get('page', get_page_parameter(pk), type=int)
    if search == 'rating':
        return jsonify(Film=MovieView.sorted_rating(page))
    if search == 'date':
        return jsonify(Film=MovieView.sorted_release_date(page))
    return jsonify(Film=MovieView.show_all_film(page))


@app.route('/add_film')
@login_required
def add_film():
    """
    Route to add new movies to the site.
    :return:
    """
    movie_title = 'A team'  # movie_title = request.form.get('movie_title')
    release_date = '2015-01-01'  # release_date = request.form.get('release_date')
    rating = 7  # rating = request.form.get('rating')
    if request.method == 'GET':  # change POST
        return jsonify(answer=add_films(movie_title=movie_title, release_date=release_date, rating=rating,
                                        id_user=current_user.id))
    return jsonify(answer=current_user.id)


@app.route('/del_films')
@login_required
def del_films():
    """
    Route to remove movies from the site.
    :return:
    """
    movie_title = 'A team'  # movie_title = request.form.get('movie_title')
    if request.method == 'GET':  # change POST
        return jsonify(answer=del_film(title=movie_title,
                                       user=current_user))
    return jsonify(answer=current_user.id)


@app.route('/login', methods=["GET", "POST"])
def login():
    """
    Route for user authorization on the site if it is in the database.
    :return:
    """
    email = 'Developer@gmail.com'  # request.form.get('email')
    password = 'python@3.10'  # request.form.get('password')
    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
        return jsonify(password='bad password.')  # flash('bad password')
    return jsonify(data_user='bad email.')  # flash('bad email.')


@app.route('/registration', methods=["GET", "POST"])
def registration():
    """
    Route for registering new users on the site
    :return:
    """
    nickname = 'Python'  # nickname = request.form.get('nickname')
    last_name = 'Wonderful'  # last_name = request.form.get('last_name')
    first_name = 'Developer'  # first_name = request.form.get('first_name')
    email = 'Developer@gmail.com'  # email = request.form.get('email')
    password = 'python@3.10'  # password = request.form.get('password')
    password2 = 'python@3.10'  # password2 = request.form.get('password')

    if request.method == 'GET':  # change POST
        return jsonify(answer=add_user(nickname, last_name, first_name, email, password, password2))
    return jsonify(Message='Go back to register')


@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    """
    Route to log out of user account.
    :return:
    """
    logout_user()
    return jsonify(answer='logout')


@app.after_request
def redirect_to_signin(response):
    """
    If the user tries to go to an address that is available only to registered users, this method will intercept him
    and redirect him to a page with the possibility of authorization after the user is successfully authorized,
    he is redirected to the page where he was.
    :param response:
    :return:
    """
    if response.status_code == 401:
        return redirect(url_for("login") + '?next=' + request.url)
    return response
