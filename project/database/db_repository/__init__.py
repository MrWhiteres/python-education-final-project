"""
Module for Abstract Repository
"""

from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    """
    Abstract Repository for custom work.
    """

    @abstractmethod
    def get(self, **kwargs):
        """Method to read one record by id"""

    @abstractmethod
    def create(self, **kwargs):
        """Method to create one record"""

    @abstractmethod
    def update(self, **kwargs):
        """Method to update one record"""

    @abstractmethod
    def delete(self, **kwargs):
        """Method to delete one record by id"""
