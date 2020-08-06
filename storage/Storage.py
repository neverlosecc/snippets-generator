from ..models import *

import logging


class Storage:
    """ Singleton Storage class, used to store all Snippet objects """

    __instance__ = None

    @staticmethod
    def get():
        if not Storage.__instance__:
            Storage.__instance__ = Storage()
        return Storage.__instance__

    def __init__(self):
        self.__list = []

    def get_all(self) -> list:
        """
        Returns all snippets
        :return: list of Snippet
        """
        return self.__list

    def insert_one(self, snippet: Snippet) -> None:
        """
        Inserting new snippet to self.__list
        :param snippet: Snippet instance
        :return: None
        """
        self.__list.append(snippet)
        logging.debug("Inserting new snippet %s.%s", snippet.table, snippet.method)
