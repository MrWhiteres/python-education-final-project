from app import app
from flask import jsonify, request, redirect, url_for
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import check_password_hash

from .contoller import add_user, add_films
from .database.models.user import User
from .views import MovieView


@app.route("/", methods=["GET", "POST"])
@app.route("/<int:page>", methods=["GET", "POST"])
def general_page():
    search = None
    page = request.args.get('page', 1, type=int)
    if search == 'rating':
        return jsonify(Film=MovieView.sorted_rating(page))
    if search == 'date':
        return jsonify(Film=MovieView.sorted_release_date(page))
    return jsonify(Film=MovieView.show_all_film(page))


@app.route('/add_film')
@login_required
def add_film():
    movie_title = 'A team'  # movie_title = request.form.get('movie_title')
    release_date = '2015-01-01'  # release_date = request.form.get('release_date')
    rating = 7  # rating = request.form.get('rating')
    if request.method == 'GET':  # change POST
        return jsonify(answer=add_films(movie_title=movie_title, release_date=release_date, rating=rating,
                                        id_user=current_user.id))
    return jsonify(answer=current_user.id)


@app.route('/login', methods=["GET", "POST"])
def login():
    email = 'Developer@gmail.com'  # request.form.get('email')
    password = 'python@3.10'  # request.form.get('password')
    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page)
        return jsonify(password='bad password.')  # flash('bad password')
    return jsonify(data_user='bad email.')  # flash('bad email.')


@app.route('/registration', methods=["GET", "POST"])
def registration():
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
    logout_user()
    return jsonify(answer='logout')


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for("login") + '?next=' + request.url)
    return response
