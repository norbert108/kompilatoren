import AST


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
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
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
            var_declaration = VariableDeclaration(type=node.type, id=init.id, line_no=init.line_no)
            inits_list.append(var_declaration)

        return inits_list

    def visit_Inits(self, node):
        return node.inits

    def visit_Fundefs(self, node):
        print "Fundefs visited"

    def visit_Instructions(self, node):
        print "Instructions visited"