from ..storage import *
from ..models import *
from ..utilities import *

import logging


class Parser:
    """ MD documentation parser """

    @staticmethod
    def parse_function(global_name: str, function_content: list) -> Snippet:
        """
        Parsing function to Snippet instance
        :param global_name: Global name of the table
        :param function_content: Splitted content from documentation, only function content
        :return: Snippet instance
        """

        logging.debug("Parsing new function from table ", global_name)

        state = {
            "parsed_function_name": False,
            "parsing_params": False,
            "parsing_ret_val": False
        }
        snippet = Snippet()
        snippet.table = global_name

        for line in function_content:
            if not state["parsed_function_name"]:
                # Is it safe? Prob not
                if "##" not in line:
                    continue
                snippet.method = str(line.split("##")[1])  # str() only because PyCharm told me to do that
                if snippet.method.startswith(" "):
                    snippet.method = snippet.method[1:]
                state["parsed_function_name"] = True
                logging.info("Processing method %s", snippet.method)
                continue

            if state["parsing_params"] or state["parsing_ret_val"]:
                # Filter out table header
                if ":-" in line or ("Name" in line and "Type" in line):
                    continue
                if "###" in line or "{%" in line or "```" in line or "##" in line:
                    state["parsing_params"] = False
                    state["parsing_ret_val"] = False
                else:
                    params = line.split("|")
                    if len(params) < 4:
                        logging.error("Table parameters was incorrect - %s", str(params))
                        raise Exception("Table parameters was incorrect")

                    param = SnippetParameter()
                    param.name = Utils.clear_table_value(params[1])
                    param.type = Utils.clear_table_value(params[2])
                    param.description = Utils.clear_table_value(params[3])
                    if len(params) > 5:
                        param.is_optional = Utils.clear_table_value(params[4]) == "-"

                    if state["parsing_params"]:
                        snippet.parameters.append(param)
                        logging.debug("Inserting new parameter %s", param.name)
                    else:
                        snippet.return_type = param
                        logging.debug("Setting return type %s", param.name)

            if "Parameters:" in line:
                state["parsing_params"] = True
            if "return value" in line.lower():
                state["parsing_ret_val"] = True

        return snippet

    @staticmethod
    def parse_content(file_name: str, md_file_content: str, is_table: bool = False) -> None:
        """
        Parsing all file content. Content -> splitted parts of functions -> Parser.parse_function for all parts
        :param file_name: File name on the git (used only for debugging)
        :param md_file_content: Full markdown content of the file
        :param is_table: Is it a table, if true function wouldn't search for global instance
        :return: None
        """

        global_name = "ERR_SOMETHING_WENT_WRONG"
        functions = list()
        current_func = list()
        state = {
            "found_functions_list": False,
            "parsing_global_name": False
        }

        for line in md_file_content.splitlines():
            if not state["found_functions_list"]:
                if not is_table:
                    if line.startswith("{% hint style=\"info\" %}"):
                        state["parsing_global_name"] = True
                    if state["parsing_global_name"]:
                        params = line.split("`")
                        if len(params) >= 4:
                            state["parsing_global_name"] = False
                            global_name = params[3]
                else:
                    if not state["parsing_global_name"]:
                        try:
                            global_name = line.split("##")[1]
                        except IndexError:
                            global_name = line.split("#")[1]  # ouch
                        if global_name.startswith(" "):
                            global_name = global_name[1:]
                        state["parsing_global_name"] = True
                        logging.info("Parsing %s from %s", global_name, file_name)
                if "##" in line.lower() and "functions" in line.lower():
                    state["found_functions_list"] = True
                continue

            if global_name == "ERR_SOMETHING_WENT_WRONG":
                logging.warning("Global name wasn't found for file %s", file_name)
                return

            if line == "":
                continue

            if line == "```":
                functions.append(current_func)
                current_func = list()
            else:
                current_func.append(line)

        for func in functions:
            Storage.get().insert_one(Parser.parse_function(global_name, func))
