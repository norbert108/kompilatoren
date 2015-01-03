from symbol import return_stmt
import ast


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, ast.Node):
                            self.visit(item)
                elif isinstance(child, ast.Node):
                    self.visit(child)


# aux classes used for redefining equality operators...
class VariableDeclaration():
    '''docstring hir'''

    def __init__(self, type, id, line_no=None, column_no=None):
        self.type = type
        self.id = id
        self.line_no = line_no
        self.column_no = column_no

    def __eq__(self, other):
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
    def __init__(self, id, line_no):
        self.id = id
        self.line_no = line_no

    def __eq__(self, other):
        return self.id == other.id


class TypeChecker(NodeVisitor):
    def visit_Program(self, node):
        declared = self.visit(node.declarations)
        defined_functions = self.visit(node.fundefs)
        used_identifiers = self.visit(node.instructions)

        for used_id in used_identifiers:
            if used_id not in declared and used_id not in defined_functions:
                print "ERROR: Line {0}: '{1}' not defined in current scope.".format(used_id.line_no, used_id.id)

    def visit_Declarations(self, node):
        declared = []

        for declaration in node.declarations:
            inits_list = self.visit(declaration)
            for init in inits_list:
                if init in declared:
                    prev_decl = declared[declared.index(init)]
                    print "ERROR: Line {0}: '{1}' redefined. Previous declaration in line {2}."\
                        .format(init.line_no, init.id, prev_decl.line_no)
            declared.extend(inits_list)
        return declared

    def visit_Declaration(self, node):
        inits_list = []
        for init in self.visit(node.inits):

            if init.expression is not None:
                self.visit(init.expression)

            # multiple declarations checking
            var_declaration = VariableDeclaration(type=node.type, id=init.id, line_no=init.line_no)
            inits_list.append(var_declaration)

        return inits_list

    def visit_ConstExpression(self, node):
        return type(node.value).__name__

    def visit_IdExpression(self, node):
        # return VariableUsage(node.id)
        pass

    def visit_BinaryExpression(self, node):
        left_result_type = self.visit(node.left)
        right_result_type = self.visit(node.right)

        # if error occurred in lower level, all expression is invalid, do not check it further
        if left_result_type is None or right_result_type is None:
            return None

        result_type = self.return_type(left_result_type, right_result_type, node.op)
        if result_type is None:
            print "ERROR: Line {0}: Argument types '{1}' and '{2}' are invalid for operation '{3}'"\
                .format(node.line_no, left_result_type, right_result_type, node.op)

        return result_type

    def visit_InsideExpression(self, node):
        return self.visit(node.expression)

    def visit_Inits(self, node):
        return node.inits

    def visit_Fundefs(self, node):
        declared = []
        for fundef in node.fundefs:
            fundef = self.visit(fundef)
            if fundef in declared:
                prev_decl = declared[declared.index(fundef)]
                print "ERROR: Line {0}: Multiple declaration of function '{1}'. Previous declaration in line {2}."\
                    .format(fundef.line_no, fundef.id, prev_decl.line_no)
            declared.append(fundef)
        return declared

    def visit_Fundef(self, node):
        if type(node.args_list_or_empty) == ast.ArgsList:
            args_list = self.visit(node.args_list_or_empty)
        else:
            args_list = None

        self.visit(node.compound_instr)

        return FunctionDeclaration(node.type, node.id, args_list=args_list, line_no=node.line_no)

    def visit_ArgsList(self, node):
        # check if arguments on list are unique
        unique_args = list(set(node.args_list))
        for arg in unique_args:
            indices = [i for i, x in enumerate(node.args_list) if x == arg]
            if len(indices) > 1:
                print "ERROR: Line {0}: Multiple definition of argument '{1} {2}'."\
                    .format(node.line_no, arg.type, arg.id)

        return node.args_list

    # instructions
    def visit_Instructions(self, node):
        used_identifiers = []
        for instruction in node.instructions:
            ret_val = self.visit(instruction)
            if isinstance(ret_val, UsedIdentifier):
                used_identifiers.append(ret_val)

        return used_identifiers

    def visit_PrintInstr(self, node):
        self.visit(node.expression)

    def visit_LabeledInstr(self, node):
        # check id usage
        self.visit(node.instruction)

    def visit_Assignment(self, node):
        self.visit(node.expression)
        return UsedIdentifier(node.id.id, node.id.line_no)

    def visit_ChoiceInstr(self, node):
        pass

    def visit_WhileInstr(self, node):
        pass

    def visit_RepeatInstr(self, node):
        pass

    def visit_ReturnInstr(self, node):
        pass

    def visit_BreakInstr(sefl, node):
        pass

    def visit_ContinueInstr(self, node):
        pass

    def visit_CompoundInstr(self, node):
        declared = self.visit(node.declarations)
        used_identifiers = self.visit(node.instructions)

        for used_id in used_identifiers:
            if used_id not in declared:
                print "ERROR: Line {0}: '{1}' not defined in current scope.".format(used_id.line_no, used_id.id)

    # auxillary functions
    def return_type(self, left, right, operation):
        returned_type = {'Integer': {}, 'Float': {}, 'String': {}}
        for i in returned_type.keys():
            returned_type[i] = {}
            for j in returned_type.keys():
                returned_type[i][j] = {}
                for k in ['+', '-', '/', '*']:
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

        return returned_type[left][right][operation]
