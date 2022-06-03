"""
Module will be responsible for filling the database with custom values.
"""
from sqlalchemy.exc import IntegrityError, PendingRollbackError


def add_inform():
    """
    function that performs the role of filling data.
    :return:
    """
    from .. import db
    from .models import role
    role_1 = role.Role('user')
    role_2 = role.Role('admin')
    try:
        role_1.save_to_db()
        role_2.save_to_db()
    except (IntegrityError, PendingRollbackError):
        pass
