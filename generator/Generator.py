import json
import pathlib
import logging

from ..storage import *


class Generator:
    """ Singleton class Generator, needed to save all parsed functions from documentation """

    __instance__ = None

    @staticmethod
    def get():
        """
        Get singleton instance
        :return: Generator instance
        """
        if not Generator.__instance__:
            Generator.__instance__ = Generator()
        return Generator.__instance__

    def __init__(self):
        self.generated = {}

    def generate(self) -> None:
        """
        Filling self.generated field with serialized Snippet objects
        :return: None
        """
        for snippet in Storage.get().get_all():
            args = ""
            arg_idx = 1
            for arg in snippet.parameters:
                args += "${" + str(arg_idx) + ":" + arg.type + " " + arg.name
                if arg.is_optional:
                    args += " (optional)"
                args += "}, "
                arg_idx += 1
            args = args[:-2]

            full_method = snippet.table + "." + snippet.method
            logging.debug("Serializing %s", full_method)

            self.generated[full_method] = {
                "prefix": full_method,
                "body": [
                    full_method + "(" + args + ")"
                ]
            }
            if snippet.return_type.type != "":
                self.generated[full_method]["description"] = "Returns " + snippet.return_type.description + " ( " + \
                                                             snippet.return_type.type + " )"

    def write(self, file_name) -> None:
        """
        Saving all serialized values from self.generated to provided file
        :param file_name: File name
        :return: None
        """
        logging.debug("Dumping serialized content to", file_name)
        with open(str(pathlib.Path(__file__).parent.parent / file_name), "w") as f:
            f.write(json.dumps(self.generated, indent=4))
