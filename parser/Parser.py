import logging

from ..models import *
from ..storage import *
from ..utilities import *


class Parser:
    """ MD documentation parser """

    @staticmethod
    def parse_function(
            global_name: str, function_content: list, is_ptr: bool = False
    ) -> list:
        """
        Parsing function to Snippet instance
        :param global_name: Global name of the table
        :param function_content: Splitted content from documentation, only field/function content
        :param is_ptr: Is table is a pointer to a class instance, if true : else .
        :return: List of snippets/fields
        """

        logging.debug("Parsing new function from table %s", global_name)

        state = {
            "parsed_function_name": False,
            "parsing_params": False,
            "parsing_ret_val": False,
            "parsing_fields": False,
        }

        return_values = {"snippet": Snippet(), "fields": []}
        return_values["snippet"].table = global_name
        return_values["snippet"].is_ptr = is_ptr

        for line in function_content:
            if "Fields:" in line:
                state["parsed_function_name"] = True
            if not state["parsed_function_name"]:
                # Is it safe? Prob not
                if "##" not in line:
                    continue
                return_values["snippet"].method = str(
                    line.split("##")[1]
                )  # str() only because PyCharm told me to
                # do that
                if return_values["snippet"].method.startswith(" "):
                    return_values["snippet"].method = return_values["snippet"].method[
                                                      1:
                                                      ]
                state["parsed_function_name"] = True
                # logging.info("Processing method %s", return_values["snippet"].method)
                continue

            if (
                    state["parsing_params"]
                    or state["parsing_ret_val"]
                    or state["parsing_fields"]
            ):
                # Filter out table header
                if ":-" in line or ("Name" in line and "Type" in line):
                    continue
                if "###" in line or "{%" in line or "```" in line or "##" in line:
                    state["parsing_params"] = False
                    state["parsing_ret_val"] = False
                    state["parsing_fields"] = False
                else:
                    params = line.split("|")
                    if len(params) < 4:
                        logging.error(
                            "Table parameters was incorrect - %s", str(params)
                        )
                        raise Exception("Table parameters was incorrect")

                    param = SnippetParameter()
                    param.name = Utils.clear_table_value(params[1])
                    param.type = Utils.clear_table_value(params[2])
                    param.description = Utils.clear_table_value(params[3])
                    if len(params) > 5:
                        param.is_optional = Utils.clear_table_value(params[4]) == "-"

                    if state["parsing_params"]:
                        return_values["snippet"].parameters.append(param)
                        logging.debug("Inserting new parameter %s", param.name)
                    elif state["parsing_ret_val"]:
                        return_values["snippet"].return_type = param
                        logging.debug("Setting return type %s", param.name)
                    elif state["parsing_fields"]:
                        field = Field()
                        field.table = global_name
                        field.field_name = param.name
                        field.field_description = param.description
                        field.is_ptr = False
                        return_values["fields"].append(field)

            if "Parameters:" in line:
                state["parsing_params"] = True
            if "return value" in line.lower():
                state["parsing_ret_val"] = True
            if "Fields:" in line:
                state["parsing_fields"] = True

        ret = []
        if return_values["snippet"].method != "":
            ret.append(return_values["snippet"])
        if len(return_values["fields"]) > 0:
            ret = [*ret, *return_values["fields"]]
        return ret

    @staticmethod
    def parse_content(
            file_name: str,
            md_file_content: str,
            is_table: bool = False,
            table_name: str = None,
    ) -> None:
        """
        Parsing all file content. Content -> splitted parts of functions -> Parser.parse_function for all parts
        :param file_name: File name on the git (used only for debugging)
        :param md_file_content: Full markdown content of the file
        :param is_table: Is it a table, if true function wouldn't search for global instance
        :param table_name: Global table name ( if known )
        :return: None
        """

        global_name = "ERR_SOMETHING_WENT_WRONG"
        if table_name:
            global_name = table_name
        functions = list()
        current_func = list()
        state = {
            "found_functions_list": False,
            "found_fields_list": False,
            "parsing_global_name": False,
        }

        for line in md_file_content.splitlines():
            if not state["found_functions_list"] and not state["found_fields_list"]:

                gname_wasnt_found = global_name == "ERR_SOMETHING_WENT_WRONG"

                if not is_table:
                    if line.startswith('{% hint style="info" %}'):
                        state["parsing_global_name"] = True
                    if state["parsing_global_name"]:
                        params = line.split("`")
                        if len(params) >= 4:
                            state["parsing_global_name"] = False
                            global_name = params[3]
                elif global_name == "ERR_SOMETHING_WENT_WRONG":
                    if not state["parsing_global_name"]:
                        try:
                            global_name = line.split("##")[1]
                        except IndexError:
                            global_name = line.split("#")[1]  # ouch
                        if global_name.startswith(" "):
                            global_name = global_name[1:]
                        state["parsing_global_name"] = True

                if gname_wasnt_found and global_name != "ERR_SOMETHING_WENT_WRONG":
                    logging.info("Parsing %s from %s", global_name, file_name)

                should_continue = True

                if "##" in line and "Functions" in line:
                    state["found_functions_list"] = True
                if "##" in line and "Fields" in line:
                    state["found_fields_list"] = True
                    should_continue = False

                if should_continue:
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

        if len(current_func) > 0:
            functions.append(current_func)

        result = [Parser.parse_function(global_name, func, not is_table) for func in functions]
        [Storage.get().insert_many(*chunk) for chunk in result]
