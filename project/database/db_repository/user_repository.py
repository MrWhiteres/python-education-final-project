"""
Module for working with a table in the user database.
"""
from . import AbstractRepository, ABC, abstractmethod
from ..models.user import User


class AbstractUserRepository(ABC):
    """
    Abstract User Repository.
    """
    @abstractmethod
    def profile_user(self, profile_id):
        """ABC method for UserRepository.profile_user"""

    @abstractmethod
    def add_new_user(self, param):
        """ABC method for UserRepository.add_new_user"""

    @abstractmethod
    def get_user(self, user_email):
        """ABC method for UserRepository.get_user"""

    @abstractmethod
    def rollback_user(self, user: User):
        """ABC method for UserRepository.rollback_user"""



class UserRepository(AbstractRepository, AbstractUserRepository):
    """
    User repository.
    """

    @staticmethod
    def add_new_user(nickname: str, last_name: str, first_name: str,
                     email: str, password: str) -> User:
        """
        Method performs the role of creating a new user in the database.
        :param nickname:
        :param last_name:
        :param first_name:
        :param email:
        :param password:
        :return:
        """
        user: User = User(nickname=nickname, last_name=last_name,
                            first_name=first_name, email=email, password=password)
        user.save_to_db()
        return user

    @staticmethod
    def rollback_user(user: User):
        """
        Method rolls back the change in the users table.
        :param user:
        :return:
        """
        user.rollback()

    @staticmethod
    def profile_user(id_user: int) -> list[User | None]:
        """
        Method returns the user object by its ID.
        :param id_user:
        :return:
        """
        return User.query.filter_by(id=id_user).first()

    @staticmethod
    def get_user(user_email) -> list[User | None]:
        """
        Method returns the user object by its email.
        :param user_email:
        :return:
        """
        return User.query.filter_by(email=user_email).first()
