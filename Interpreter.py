import copy

import AST
from Memory import *
from Exceptions import *
from Identifiers import *
from visit import *


class Interpreter(object):

    def __init__(self):
        self.local_vars = MemoryStack()
        self.global_vars = MemoryStack()
        self.functions = {}
        self.call_stack = []

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        # declare global variables
        node.declarations.accept2(self)
        global_vars = self.local_vars.pop()
        self.global_vars.push(global_vars)

        if node.fundefs is not None:
            node.fundefs.accept2(self)
        # print self.functions

        node.instructions.accept2(self)

    @when(AST.Declarations)
    def visit(self, node):
        self.local_vars.push(Memory())

        for declaration in node.declarations:
            declaration.accept2(self)

    @when(AST.Declaration)
    def visit(self, node):
        node.inits.accept2(self)

    @when(AST.ConstExpression)
    def visit(self, node):
        return node.value

    @when(AST.IdExpression)
    def visit(self, node):
        if self.local_vars.has_key(node.id):
            id_value = self.local_vars.get(node.id)
        else:
            id_value = self.global_vars.get(node.id)

        return id_value

    @when(AST.BinaryExpression)
    def visit(self, node):
        left_node = node.left.accept2(self)
        if type(left_node) == AST.ConstExpression:
            left = left_node.value
        else:
            left = left_node
        left_type = type(left).__name__

        right_node = node.right.accept2(self)
        if type(right_node) == AST.ConstExpression:
            right = right_node.value
        else:
            right = right_node
        right_type = type(right).__name__

        operator = node.op

        res_type = result_type(left_type, right_type, node.op)
        if res_type is None:
            return None

        # perform operation...
        result = None
        if operator == '+':
            result = left.value + right.value
        elif operator == '-':
            result = left.value - right.value
        elif operator == '*':
            result = left.value * right.value
        elif operator == '/':
            try:
                result = left.value / right.value
            except ZeroDivisionError:
                print "Line {0}: Division by 0.".format(node.line_no)
                return None
        elif operator == '%':
            try:
                result = left.value % right.value
            except ZeroDivisionError:
                print "Line {0}: Division by 0.".format(node.line_no)
                return None
        elif operator == '==':
            result = left.value == right.value
        elif operator == '!=':
            result = left.value != right.value
        elif operator == '>=':
            result = left.value >= right.value
        elif operator == '<=':
            result = left.value <= right.value
        elif operator == '>':
            result = left.value > right.value
        elif operator == '<':
            result = left.value < right.value
        elif operator == '|':
            result = left.value | right.value
        elif operator == '&':
            result = left.value & right.value
        elif operator == '^':
            result = left.value ^ right.value
        elif operator == '>>':
            result = left.value >> right.value
        elif operator == '<<':
            result = left.value << right.value
        elif operator == '&&':
            result = left.value and right.value
        elif operator == '||':
            result = left.value and right.value

        # create result node
        if res_type == 'Integer':
            res_node =AST.Integer(result)
        elif res_type == 'Float':
            res_node = AST.Float(result)
        elif res_type == 'String':
            res_node = AST.String(result)
        else:
            res_node = AST.Boolean(result)

        return res_node

    @when(AST.FunctionExpression)
    def visit(self, node):
        func_def = self.functions.get(node.id)

        # evaluate input parameters, add them to function scope (as globals, because shadowing, that's why)
        call_params = node.expression.accept2(self)
        args_list = func_def.args_list_or_empty.accept2(self)

        tmp = self.global_vars.pop()
        func_global_scope = copy.copy(tmp)
        self.global_vars.push(tmp)

        for i in xrange(len(args_list)):
            func_global_scope.variables[args_list[i]] = call_params[i]

        self.global_vars.push(func_global_scope)

        # actual call
        ret_val = None
        try:
            func_def.accept2(self)
        except ReturnValueException as re:
            ret_val = re.value
            self.global_vars.pop()

        return ret_val

    @when(AST.ExpressionList)
    def visit(self, node):
        call_params = []
        for expr in node.expr_list:
            if issubclass(type(expr), AST.Expression):
                expr_val = expr.accept2(self)
                call_params.append(expr_val)
            else:
                call_params.append(expr)
        return call_params

    @when(AST.InsideExpression)
    def visit(self, node):
        res = node.expression.accept2(self)
        return res

    @when(AST.Inits)
    def visit(self, node):
        for init in node.inits:
            init.accept2(self)

    @when(AST.Init)
    def visit(self, node):
        value = None
        if node.expression is not None:
            value = node.expression.accept2(self)
            if type(value) == AST.ConstExpression:
                value = value.value
        self.local_vars.set(node.id, value)

    @when(AST.Fundefs)
    def visit(self, node):
        for fundef in node.fundefs:
            self.functions[fundef.id] = fundef

    @when(AST.Fundef)
    def visit(self, node):
        node.compound_instr.accept2(self)

    @when(AST.ArgsList)
    def visit(self, node):
        args_names = []
        for arg in node.args_list:
            args_names.append(arg.id)
        return args_names

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept2(self)

    @when(AST.PrintInstr)
    def visit(self, node):
        text = node.expression.accept2(self)
        print '{0}'.format(text.value)

    @when(AST.LabeledInstr)
    def visit(self, node):
        pass

    @when(AST.Assignment)
    def visit(self, node):
        id = node.id.id

        # if variable is not found on local stack, then its global
        if not self.local_vars.has_key(id):
            variable_stack = self.global_vars
        else:
            variable_stack = self.local_vars

        right_side = node.expression.accept2(self)
        if type(right_side) == AST.ConstExpression:
            right_val = right_side.value
        else:
            right_val = right_side

        variable_stack.set(id, right_val)

    @when(AST.ChoiceInstr)
    def visit(self, node):
        condition = node.condition.accept2(self).value
        if condition:
            node.instruction.accept2(self)
        elif node.else_instruction is not None:
            node.else_instruction.accept2(self)

    @when(AST.WhileInstr)
    def visit(self, node):
        while True:
            condition = node.condition.accept2(self).value
            if condition:
                try:
                    node.instruction.accept2(self)
                except BreakException:
                    break
                except ContinueException:
                    continue
            else:
                break

    @when(AST.RepeatInstr)
    def visit(self, node):
        pass

    @when(AST.ReturnInstr)
    def visit(self, node):
        value = node.expression.accept2(self)
        raise ReturnValueException(value)

    @when(AST.BreakInstr)
    def visit(self, node):
        raise BreakException

    @when(AST.ContinueInstr)
    def visit(self, node):
        raise ContinueException

    @when(AST.CompoundInstr)
    def visit(self, node):
        # create local variables
        node.declarations.accept2(self)

        try:
            node.instructions.accept2(self)
        except ReturnValueException as re:
            self.local_vars.pop()
            raise ReturnValueException(re.value)

        # out of instruction block, destroy local variables
        self.local_vars.pop()
