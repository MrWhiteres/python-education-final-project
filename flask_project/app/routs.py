from flask import jsonify, request
from flask_login import login_required, logout_user, login_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from . import app
from .database.models.user import User


@app.route("/")
def ip():
    from socket import gethostbyname, getfqdn
    ip_user = gethostbyname(getfqdn())
    return jsonify(ip_user=ip_user)


@app.route('/login_page', methods=["GET", "POST"])
def login():
    email = 'Developer@gmail.com'  # request.form.get('email')
    password = 'python@3.10'  # request.form.get('password')
    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify(welcom_back=user.nickname)
        return jsonify(password='bad password.')
    return jsonify(data_user='bad login or password.')


@app.route('/registration', methods=["GET", "POST"])
def registration():
    nickname = 'Python'  # nickname = request.form.get('nickname')
    last_name = 'Wonderful'  # last_name = request.form.get('last_name')
    first_name = 'Developer'  # first_name = request.form.get('first_name')
    email = 'Developer@gmail.com'  # email = request.form.get('email')
    password = 'python@3.10'  # password = request.form.get('password')
    password2 = 'python@3.10'  # password2 = request.form.get('password')

    if request.method == 'GET':  # change POST
        if not (nickname or last_name or first_name or email or password or password2):
            return jsonify(answer='Please, fill all fields!')  # flash('Please, fill all fields!')
        elif password != password2:
            return jsonify(answer='Passwords are not equal!')  # flash('Passwords are not equal!')
        else:
            try:
                hash_pwd = generate_password_hash(password)
                new_user = User(nickname=nickname, last_name=last_name, first_name=first_name, email=email,
                                password=hash_pwd)
                new_user.save_to_db()
                return jsonify(user=f"'{new_user.nickname}' created.")
            except IntegrityError:
                return jsonify(answer=f"user '{new_user.nickname}' already exist.")

    return jsonify(Message='Go back to register')


@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return jsonify(answer='logout')