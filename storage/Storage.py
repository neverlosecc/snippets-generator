import logging

from ..models import *


class Storage:
    """ Singleton Storage class, used to store all Snippet objects """

    __instance__ = None

    @staticmethod
    def get():
        if not Storage.__instance__:
            Storage.__instance__ = Storage()
        return Storage.__instance__

    def __init__(self):
        self._snippets = []
        self._fields = []

    def get_snippets(self) -> list:
        """
        Returns all snippets
        :return: list of Snippet
        """
        return self._snippets

    def get_fields(self) -> list:
        """
        Returns all fields
        :return: list of Field
        """
        return self._fields

    def insert_one(self, value: Snippet or Field) -> None:
        """
        Inserting new snippet or field to storage
        :param value: Snippet or Field instance
        :return: None
        """
        if isinstance(value, Snippet):
            logging.debug("Inserting new snippet: %s.%s", value.table, value.method)
            self._snippets.append(value)
        elif isinstance(value, Field):
            logging.debug("Inserting new field: %s.%s", value.table, value.field_name)
            self._fields.append(value)
        else:
            logging.error("Value type wasn't Snippet or Field")

    def insert_many(self, *args) -> None:
        """
        Inserting multiply snippets/fields to storage
        :param args: Values
        :return: None
        """
        for val in args:
            self.insert_one(val)
