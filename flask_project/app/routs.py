"""
Module implements all the paths of the address bar in the flask application.
"""
from flask import jsonify, request, redirect, url_for
from flask_login import login_required, logout_user, current_user
from flask_paginate import get_page_parameter

from .app import app
from .contoller import init_add_film, general_page_views, init_del_film, init_login_user, \
    init_add_user, search_films


@app.route("/", methods=["GET", "POST"])
@app.route("/<int:pk>", methods=["GET", "POST"])
def general_page(pk=1):
    page: int = request.args.get('page', get_page_parameter(pk), type=int)
    if request.method == 'GET':
        return jsonify(Film=general_page_views("GET", page))
    if request.method == "POST":
        return jsonify(Film=general_page_views("POST", page))


@app.route('/add_film', methods=["GET", "POST"])
@login_required
def add_film():
    """
    Route to add new movies to the site.
    :return:
    """
    if request.method == 'GET':
        return jsonify(answer=init_add_film(method='GET', user_id=current_user.id))
    if request.method == 'POST':
        return jsonify(answer=init_add_film(method='POST', user_id=current_user.id))


@app.route('/del_films', methods=['GET', 'POST'])
@login_required
def del_films():
    """
    Route to remove movies from the site.
    :return:
    """
    if request.method == 'GET':
        return jsonify(answer=init_del_film('GET', current_user))
    if request.method == 'POST':
        return jsonify(answer=init_del_film('POST', current_user))


@app.route('/login', methods=["POST"])
def login():
    """
    Route for user authorization on the site if it is in the database.
    :return:
    """
    if request.method == "POST":
        return jsonify(answer=init_login_user())


@app.route('/registration', methods=["POST"])
def registration():
    """
    Route for registering new users on the site
    :return:
    """
    if request.method == 'POST':  # change POST
        return jsonify(answer=init_add_user())


@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    """
    Route to log out of user account.
    :return:
    """
    user: str = current_user.nickname
    logout_user()
    return jsonify(answer=f"Come back, {user}")

@app.route('/search', methods=["GET", "POST"])
@app.route('/search/<search>', methods=["GET", "POST"])
def search(search):
    if request.method == "GET":
        return jsonify(answer=search_films("GET", search))
    if request.method == "POST":
        return jsonify(answer=search_films('POST'))

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
