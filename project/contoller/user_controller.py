"""
Module is a controller initializer for operations with users.
"""

from flask_login import login_user
from sqlalchemy.exc import PendingRollbackError, IntegrityError
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from ..database.db_repository.user_repository import AbstractUserRepository
from ..database.forms.user_form import LoginForm
from ..database.forms.user_form import RegistrationForm
from ..database.models.user import User
from ..logger import logger


def profile(users: User, profile_id: int, repository: AbstractUserRepository) -> dict[str, str] | tuple[str, int]:
    """
    Function checks the user id and his role then returns the data.
    :param repository:
    :param users:
    :param profile_id:
    :return:
    """
    if users.id == profile_id or users.role.role_name == 'admin':
        user = repository.profile_user(profile_id)
        if user:
            logger.info(f"<{users.nickname}/{users.role.role_name}>,"
                        f" show profile user<'{user.nickname}, user if - {profile_id}'>.")
            return {'Nickname': user.nickname, 'Last Name': user.last_name,
                    'First Name': user.first_name, 'Email': user.email, 'Role': user.role.role_name}
        return "User not found.", 204

    logger.error(f"The user - '{users.nickname}' tried to view information inaccessible to him.")
    return "There's nothing here.", 403


def init_add_user(data: dict, repository: AbstractUserRepository) -> tuple[str, int]:
    """
    Function collects information and then passes it to create a new user.
    :return:
    """
    if not data["nickname"] or not data["last_name"] or not data["first_name"] \
            or not data["email"] or not data["password"] or not data["password2"]:
        return 'Please, fill all fields!', 409

    if data["password"] != data["password2"]:
        return 'Passwords are not equal!', 409

    form_input = ImmutableMultiDict(data)
    if RegistrationForm(form_input).validate():

        data["password"] = generate_password_hash(data["password"])
        del data["password2"]

        try:
            new_user: User = repository.add_new_user(**data)
            logger.info(f"New user add to db - '{new_user.nickname}'.")
            return f"'{new_user.nickname}' created.", 201

        except (IntegrityError, PendingRollbackError):
            logger.error("Registration of user failed, user already exists.")
            return "User already exist.", 403

    logger.error(f"An error occurred while registering a new user, incorrect data.- {data['nickname']}")
    return 'Incorrect data', 409


def init_login_user(data: dict, repository: AbstractUserRepository) -> tuple[str, int]:
    """
    Function collects user information and then passes i to check if such a user is in the database.
    :return:
    """
    form_input = ImmutableMultiDict(data)
    if not LoginForm(form_input).validate():
        return 'Please, fill all fields!', 409

    user = repository.get_user(user_email=data["email"])

    if user and check_password_hash(user.password, data["password"]):
        login_user(user)
        logger.info(f"User logged in '{user.nickname}'")
        return "Welcome back.", 200

    logger.error(f"An attempt was made to log in to a user account - '{user.nickname if user else None}'.")
    return 'Incorrect data', 409
