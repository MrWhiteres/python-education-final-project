from flask_restx import fields

from .app import api

registration_user_model = api.model('User registration', {
    'nickname': fields.String(default=None),
    'last_name': fields.String(default=None),
    'first_name': fields.String(default=None),
    'email': fields.String(default=None),
    'password': fields.String(default=None),
    'password2': fields.String(default=None)
})

login_user_model = api.model('User login', {
    'email': fields.String(default=None),
    'password': fields.String(default=None),
})


film_model = api.model('Film Model', {
    'movie_title': fields.String(default=None),
    'release_date': fields.Date(default=None),
    'rating': fields.Integer(default=None),
    'poster': fields.String(default=None),
    'description': fields.String(default=None),
    'genre': fields.List(fields.String(default=None), default=None),
    'id_director': fields.Integer(default=None)
})

film_edit_model = api.model('Films edit model', {
    "movie_title": fields.String(default=None),
    "release_date": fields.Date(default=None),
    "rating": fields.Integer(default=None),
    "poster": fields.String(default=None),
    "description": fields.String(default=None),
})

del_film_model = api.model('Film dell', {
    'movie_title': fields.String(default=None)
})


general_page_model = api.model('General Page', {
    "filters": fields.List(fields.String(default=None), default=None),
    "sorted_methods": fields.List(fields.String(default=None), default=None),
    "genres": fields.List(fields.String(default=None), default=None),
    "paginate": fields.Integer(default=None),
    "director_id": fields.List(fields.Integer(default=None), default=None),
    "min_date": fields.Date(default=None),
    "max_date": fields.Date(default=None),
})
