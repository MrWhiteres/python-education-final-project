"""
Module stores the object model user.
"""
from flask_login import UserMixin

from . import db, BaseModel
from ...app import login_manager
from .role import Role


class User(db.Model, BaseModel, UserMixin):
    """
    Class is the schema for the user table.
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nickname = db.Column(db.String(255), nullable=False, unique=True)
    last_name = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    id_role = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role")

    def __init__(self, nickname, last_name, first_name, email, password, id_role):
        self.nickname = nickname
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.password = password
        self.id_role = id_role

    def __repr__(self):
        return f'<cls-User ({self.id}, {self.nickname}, {self.role.role_name})>'


@login_manager.user_loader
def load_user(user_id):
    """
    Function is responsible for loading the user session.
    :param user_id:
    :return:
    """
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_handler():
    """
    If user not log in
    """
    return 'Unauthorized', 401