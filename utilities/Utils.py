class Utils:
    @staticmethod
    def clear_table_value(value) -> str:
        """
        As you can see, markdown tables have spaces before content of the row, so we'll remove that spaces
        Also it will clear all "\" symbols from file due to markdown standarts
        :param value: Markdown table row value
        :return: str
        """
        if value.startswith(" ") or value.startswith("\t"):
            value = value[1:]
        if value.endswith(" ") or value.endswith("\t"):
            value = value[:-1]
        return value.replace("\\", "")
