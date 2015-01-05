# aux classes used for redefining equality operators...
class VariableDeclaration():
    '''docstring hir'''

    def __init__(self, type, id, line_no=None, column_no=None):
        self.type = type
        self.id = id
        self.line_no = line_no
        self.column_no = column_no

    def __eq__(self, other):
        if isinstance(other, UsedIdentifier):
            return self.id == other.id
        return self.type == other.type and self.id == other.id


class FunctionDeclaration():
    ''' j.w. '''

    def __init__(self, type, id, args_list, line_no=None):
        self.type = type
        self.id = id
        self.args_list = args_list
        self.line_no = line_no

    def __eq__(self, other):
        return self.type == other.type and self.id == other.id and self.args_list == other.args_list


class UsedIdentifier():
    def __init__(self, id, line_no=None):
        self.id = id
        self.line_no = line_no

    def __eq__(self, other):
        return self.id == other.id