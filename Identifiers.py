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


def result_type(left, right, operation):
    left = left[0].upper() + left[1:]
    right = right[0].upper() + right[1:]

    returned_type = {'Integer': {}, 'Float': {}, 'String': {}, 'Boolean': {}}
    for i in returned_type.keys():
        returned_type[i] = {}
        for j in returned_type.keys():
            returned_type[i][j] = {}
            for k in ['+', '-', '/', '*', '==', '>=', '<=', '!=']:
                returned_type[i][j][k] = None

    returned_type['Integer']['Float']['+'] = 'Float'
    returned_type['Integer']['Integer']['+'] = 'Integer'
    returned_type['Float']['Float']['+'] = 'Float'
    returned_type['Float']['Integer']['+'] = 'Float'
    returned_type['String']['String']['+'] = 'String'
    returned_type['Integer']['Float']['-'] = 'Float'
    returned_type['Integer']['Integer']['-'] = 'Integer'
    returned_type['Float']['Float']['-'] = 'Float'
    returned_type['Float']['Integer']['-'] = 'Float'
    returned_type['Integer']['Float']['*'] = 'Float'
    returned_type['Integer']['Integer']['*'] = 'Integer'
    returned_type['Float']['Float']['*'] = 'Float'
    returned_type['Float']['Integer']['*'] = 'Float'
    returned_type['String']['Integer']['*'] = 'String'
    returned_type['Integer']['Float']['/'] = 'Float'
    returned_type['Integer']['Integer']['/'] = 'Integer'
    returned_type['Float']['Float']['/'] = 'Float'
    returned_type['Float']['Integer']['/'] = 'Float'
    returned_type['Float']['Float']['=='] = 'Boolean'
    returned_type['Integer']['Integer']['=='] = 'Boolean'
    returned_type['String']['String']['=='] = 'Boolean'
    returned_type['Float']['Float']['!='] = 'Boolean'
    returned_type['Integer']['Integer']['!='] = 'Boolean'
    returned_type['String']['String']['!='] = 'Boolean'
    returned_type['Float']['Float']['>='] = 'Boolean'
    returned_type['Integer']['Integer']['>='] = 'Boolean'
    returned_type['String']['String']['>='] = 'Boolean'
    returned_type['Float']['Float']['<='] = 'Boolean'
    returned_type['Integer']['Integer']['<='] = 'Boolean'
    returned_type['String']['String']['<='] = 'Boolean'
    returned_type['Float']['Integer']['=='] = 'Boolean'
    returned_type['Integer']['Float']['=='] = 'Boolean'
    returned_type['Float']['Integer']['!='] = 'Boolean'
    returned_type['Integer']['Float']['!='] = 'Boolean'
    returned_type['Float']['Integer']['>='] = 'Boolean'
    returned_type['Integer']['Float']['>='] = 'Boolean'
    returned_type['Float']['Integer']['<='] = 'Boolean'
    returned_type['Integer']['Float']['<='] = 'Boolean'
    returned_type['Integer']['Integer']['<<'] = 'Integer'
    returned_type['Integer']['Integer']['>>'] = 'Integer'
    returned_type['Integer']['Integer']['|'] = 'Integer'
    returned_type['Integer']['Integer']['&'] = 'Integer'
    returned_type['Integer']['Integer']['^'] = 'Integer'
    returned_type['Integer']['Integer']['<'] = 'Boolean'
    returned_type['Float']['Float']['<'] = 'Boolean'
    returned_type['Float']['Integer']['<'] = 'Boolean'
    returned_type['Integer']['Float']['<'] = 'Boolean'
    returned_type['Boolean']['Boolean']['<'] = 'Boolean'
    returned_type['Float']['Float']['>'] = 'Boolean'
    returned_type['Float']['Integer']['>'] = 'Boolean'
    returned_type['Integer']['Float']['>'] = 'Boolean'
    returned_type['Boolean']['Boolean']['>'] = 'Boolean'
    returned_type['Boolean']['Boolean']['&&'] = 'Boolean'
    returned_type['Boolean']['Boolean']['||'] = 'Boolean'

    return returned_type[left][right][operation]