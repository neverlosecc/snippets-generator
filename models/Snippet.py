from .SnippetParameter import SnippetParameter


class Snippet:
    """ Snippet object, will be used to store all information about snippets """

    def __init__(self):
        self.table = ""
        self.method = ""
        self.parameters = list()
        self.return_type = SnippetParameter()
        self.is_ptr = False
