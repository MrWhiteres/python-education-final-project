"""
Module contains extensions of the model.
"""
from ...database import db, marsh


class BaseModel:
    """
    Class is engaged in the extension of all models that will be inherited from it.
    """

    def save_to_db(self):
        """
        Function will save the object to the database.
        :return:
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        Function deletes an object from the database.
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def rollback():
        """
        Function rolls back the value if an error occurs.
        :return:
        """
        db.session.rollback()
