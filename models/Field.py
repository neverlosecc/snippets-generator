class Field:
    """ Field object, used to store table fields (like CGlobalVarsBase) """

    def __init__(self):
        self.table = ""
        self.field_name = ""
        self.field_description = ""
        self.is_ptr = False
