import json
import pathlib
import logging

from ..storage import *


class Generator:
    """ Singleton class Generator, needed to save all parsed snippets/fields from documentation """

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
        Filling self.generated field with serialized Snippet and Field objects
        :return: None
        """
        for field in Storage.get().get_fields():
            body = f"{field.table}{'.' if not field.is_ptr else ':'}{field.field_name}"
            self.generated[body] = {
                "prefix": body,
                "body": [body],
                "description": field.field_description,
            }
        for snippet in Storage.get().get_snippets():
            args = ""
            arg_idx = 1
            for arg in snippet.parameters:
                args += "${" + str(arg_idx) + ":" + arg.type + " " + arg.name
                if arg.is_optional:
                    args += " (optional)"
                args += "}, "
                arg_idx += 1
            args = args[:-2]

            full_method = (
                f"{snippet.table}{'.' if not snippet.is_ptr else ':'}{snippet.method}"
            )
            logging.debug("Serializing %s", full_method)

            self.generated[full_method] = {
                "prefix": full_method,
                "body": [full_method + "(" + args + ")"],
            }
            if snippet.return_type.type != "":
                description_text = "Returns "
                found_description = False
                if snippet.return_type.description not in ["", " "]:
                    description_text += snippet.return_type.description
                    found_description = True

                if found_description:
                    description_text += " ( %s )" % snippet.return_type.type
                else:
                    # https://docs.neverlose.cc/developers/tables/antiaim#getcurrentrealrotation
                    description_text += snippet.return_type.type + (
                        " ( %s )" % snippet.return_type.name
                    )

                self.generated[full_method]["description"] = description_text

    def write(self, file_name) -> None:
        """
        Saving all serialized values from self.generated to provided file
        :param file_name: File name
        :return: None
        """
        logging.debug("Dumping serialized content to %s", file_name)
        with open(str(pathlib.Path(__file__).parent.parent / file_name), "w") as f:
            f.write(json.dumps(self.generated, indent=4))
