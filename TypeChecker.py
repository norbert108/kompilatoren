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


class VariableDeclaration():
    '''docstring hir'''

    def __init__(self, type, id, line_no=None, column_no=None):
        self.type = type
        self.id = id
        self.line_no = line_no
        self.column_no = column_no

    def __eq__(self, other):
        return self.type == other.type and self.id == other.id


class VariableUsage():
    def __init__(self, id, line_no=None):
        self.id = id
        self.line_no = line_no

    def __eq__(self, other):
        return self.id == other.id

class TypeChecker(NodeVisitor):
    def visit_Program(self, node):
        self.visit(node.declarations)
        self.visit(node.fundefs)
        self.visit(node.instructions)

    def visit_Declarations(self, node):
        declared = []

        for declaration in node.declarations:
            inits_list = self.visit(declaration)
            for init in inits_list:
                if init in declared:
                    prev_decl = declared[declared.index(init)]
                    print "ERROR: Line {0}: '{2}' redefined. Prevorious declaration in line {3}."\
                        .format(init.line_no, init.column_no, init.id, prev_decl.line_no)
            declared.extend(inits_list)

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
        return VariableUsage(node.id)

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
        print "Fundefs visited"

    def visit_Instructions(self, node):
        print "Instructions visited"

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
