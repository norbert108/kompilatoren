import AST
from Identifiers import *

class NodeVisitor(object):

    def visit(self, node, data=None):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, data=data)

    def generic_visit(self, node, data):        # Called if no explicit visitor function exists for a node.
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


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.errors = 0

    def visit_Program(self, node, data):
        declared = self.visit(node.declarations, [[], []])
        defined_functions = self.visit(node.fundefs, [declared, []])
        self.visit(node.instructions, [declared, defined_functions])
        return self.errors

    def visit_Declarations(self, node, data):
        declared = []

        for declaration in node.declarations:
            inits_list = self.visit(declaration, [data[0] + declared, data[1]])
            for init in inits_list:
                if init in declared:
                    prev_decl = declared[declared.index(init)]
                    print "Line {0}: '{1}' redefined. Previous declaration in line {2}."\
                        .format(init.line_no, init.id, prev_decl.line_no)
                    self.errors += 1
            declared.extend(inits_list)
        return declared

    def visit_Declaration(self, node, data):
        inits_list = []

        for init in self.visit(node.inits):
            if init.expression is not None:
                returned_type = self.visit(init.expression, data)
                if isinstance(returned_type, UsedIdentifier):
                    if data is not None:
                        if returned_type not in data[0]:
                            print "Line {0}: '{1}' is not defined in current scope."\
                                .format(init.line_no, returned_type.id)
                            self.errors += 1
                            continue
                        else:
                            idx = data[0].index(returned_type)
                            returned_type = (data[0])[idx].type

                if returned_type is not None:
                    var_type = node.type[0].upper() + node.type[1:]
                    if var_type == 'Int':
                        var_type = 'Integer'

                    val_type = returned_type[0].upper() + returned_type[1:]
                    if val_type == 'Int':
                        val_type = 'Integer'

                    if not (var_type == val_type or (var_type == 'Float' and val_type == 'Integer')):
                        print "ERROR: Line {0}: Type mismatch '{1}' and '{2}'."\
                            .format(init.line_no, var_type, val_type)
                        self.errors += 1
                        continue

            # multiple declarations checking
            var_declaration = VariableDeclaration(type=node.type, id=init.id, line_no=init.line_no)
            inits_list.append(var_declaration)

        return inits_list

    def visit_ConstExpression(self, node, data):
        return type(node.value).__name__

    def visit_IdExpression(self, node, data):
        return UsedIdentifier(node.id, node.line_no)

    def visit_BinaryExpression(self, node, data):
        declared_variables = None
        if data is not None:
            declared_variables = data[0]

        left_result_type = self.visit(node.left, data)
        right_result_type = self.visit(node.right, data)

        # if error occurred in lower level, all expression is invalid, do not check it further
        if left_result_type is None or right_result_type is None:
            return None

        if left_result_type is "NotDeclared" or right_result_type is "NotDeclared":
            return "NotDeclared"

        # if 'data' is None, that means no variables were declared so we are declaring them now (nothing != 0)
        if data is not None:
            if isinstance(left_result_type, UsedIdentifier):
                try:
                    variable_idx = declared_variables.index(left_result_type)
                    left_result_type = declared_variables[variable_idx].type
                except ValueError:
                    print "Line {0}: '{1}' is not declared in current scope."\
                        .format(left_result_type.line_no, left_result_type.id)
                    self.errors += 1
                    return "NotDeclared"

            if isinstance(right_result_type, UsedIdentifier):
                try:
                    variable_idx = declared_variables.index(right_result_type)
                    right_result_type = declared_variables[variable_idx].type
                except ValueError:
                    print "Line {0}: '{1}' is not declared in current scope."\
                          .format(right_result_type.line_no, right_result_type.id)
                    self.errors += 1
                    return "NotDeclared"

        res_type = result_type(left_result_type, right_result_type, node.op)
        if res_type is None:
            print "Line {0}: Argument types '{1}' and '{2}' are invalid for operation '{3}'"\
                .format(node.line_no, left_result_type, right_result_type, node.op)
            self.errors += 1

        return res_type

    def visit_FunctionExpression(self, node, data):
        if UsedIdentifier(node.id) not in data[1]:
            print "Line {0}: Function '{1}' is not defined." \
                .format(node.line_no, node.id)
            # self.errors += 1
            return

        possible_candidates = []
        for func in data[1]:
            if func.id == node.id:
                possible_candidates.append(func)
                match = self.visit(node.expression, func.args_list)
                if match:
                    return func.type

        print "Line {0}: Function '{1}' does not take parameters: ".format(node.line_no, node.id),
        for argument in node.expression.expr_list:
            if node.expression.expr_list.index(argument) != 0:
                print ",",
            print "'{0}'".format(type(argument.value).__name__),
        print ""
        print "Possible candidates are: "
        for candidate in possible_candidates:
            print "    {0} {1} (".format(candidate.type, candidate.id),
            for param in candidate.args_list:
                if candidate.args_list.index(param) != 0:
                    print ",",
                print "{0}".format(param.type),
            print ")"
        self.errors += 1

    def visit_ExpressionList(self, node, data):
        param_type = ""
        last_arg_no = 0
        for i in xrange(len(data)):
            if type(node.expr_list[i]) == AST.BinaryExpression or\
                            type(node.expr_list[i]) == AST.IdExpression or\
                            type(node.expr_list[i]) == AST.InsideExpression or\
                            type(node.expr_list[i]) == AST.FunctionExpression:
                last_arg_no += 1
                continue

            if type(node.expr_list[i].value) == AST.Integer:
                param_type = "int"
            elif type(node.expr_list[i].value) == AST.Float:
                param_type = "float"
            elif type(node.expr_list[i].value) == AST.String:
                param_type = "string"

            if param_type != data[i].type:
                return False

            last_arg_no += 1
        if last_arg_no != len(node.expr_list):
            return False
        else:
            return True

    def visit_InsideExpression(self, node, data):
        return self.visit(node.expression, data)

    def visit_Inits(self, node, data):
        return node.inits

    def visit_Fundefs(self, node, data):
        # print "FUDEFS: {0}".format(data)
        declared = []
        for fundef in node.fundefs:
            defined_functions = []
            if data is not None and len(data) > 1:
                defined_functions.extend((data[1])[:])
            defined_functions.extend(declared)

            updated_data = [data[0], defined_functions]
            # print "UPDATED DATA: {0}".format(updated_data)

            fundef = self.visit(fundef, updated_data)
            if fundef in declared:
                prev_decl = declared[declared.index(fundef)]
                print "Line {0}: Multiple declaration of function '{1}'. Previous declaration in line {2}."\
                    .format(fundef.line_no, fundef.id, prev_decl.line_no)
                self.errors += 1
            declared.append(fundef)
        return declared

    def visit_Fundef(self, node, data):

        updated_locals = (data[0])[:]
        if type(node.args_list_or_empty) == AST.ArgsList:
            args_list = self.visit(node.args_list_or_empty, data)
            for arg in args_list:
                updated_locals.append(VariableDeclaration(arg.type, arg.id))
        else:
            args_list = None

        # print "upd locals {0}".format(updated_locals[0])

        declared_functions = []
        if data is not None and len(data) > 1:
            declared_functions = (data[1])[:]
        declared_functions.append(FunctionDeclaration(node.type, node.id, args_list=args_list, line_no=node.line_no))

        updated_data = [updated_locals, declared_functions]
        self.visit(node.compound_instr, updated_data)

        return FunctionDeclaration(node.type, node.id, args_list=args_list, line_no=node.line_no)

    def visit_ArgsList(self, node, data):
        # check if arguments on list are unique
        unique_args = list(set(node.args_list))
        for arg in unique_args:
            indices = [i for i, x in enumerate(node.args_list) if x == arg]
            if len(indices) > 1:
                print "Line {0}: Multiple definition of argument '{1} {2}'."\
                    .format(node.line_no, arg.type, arg.id)
                self.errors += 1

        return node.args_list

    # instructions
    def visit_Instructions(self, node, data):
        used_identifiers = []  # reduntant?

        # if this happens it means code does not make sense
        if data is None:
            print "Too many errors"
        declared_identifiers = data[0]

        for instruction in node.instructions:
            ret_val = self.visit(instruction, data)

            # if instruction was expression that used identifiers
            if isinstance(ret_val, UsedIdentifier):
                used_identifiers.append(ret_val)
                if ret_val not in declared_identifiers:
                    print "Line {0}: '{1}' not defined in current scope.".format(ret_val.line_no, ret_val.id)
                    self.errors += 1
            elif isinstance(ret_val, AST.LabeledInstr):
                if UsedIdentifier(id=ret_val.id) in declared_identifiers:
                    print "Line {0}: Identifier '{1}' already in use.".format(ret_val.line_no, ret_val.id)
                    self.errors += 1

    def visit_PrintInstr(self, node, data):
        self.visit(node.expression, data)

    def visit_LabeledInstr(self, node, data):
        self.visit(node.instruction, data)
        return node

    def visit_Assignment(self, node, data):
        self.visit(node.expression, data)
        return self.visit(node.id, data)

    def visit_ChoiceInstr(self, node, data):
        self.visit(node.condition, data)
        self.visit(node.instruction, data)
        if node.else_instruction is not None:
            self.visit(node.else_instruction, data)

    def visit_WhileInstr(self, node, data):
        self.visit(node.condition, data)
        self.visit(node.instruction, data)

    def visit_RepeatInstr(self, node, data):
        self.visit(node.condition, data)
        self.visit(node.instructions, data)

    def visit_ReturnInstr(self, node, data):
        self.visit(node.expression, data)

    def visit_BreakInstr(sefl, node, data):
        pass

    def visit_ContinueInstr(self, node, data):
        pass

    def visit_CompoundInstr(self, node, data):
        function_definitions = []
        if data is not None and len(data) > 1:
            function_definitions = data[1]

        local_variables = self.visit(node.declarations, data)
        all_locals = data[0] + local_variables

        updated_data = [all_locals, function_definitions]
        self.visit(node.instructions, updated_data)
