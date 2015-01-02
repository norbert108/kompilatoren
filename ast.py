class Node(object):
    def __str__(self):
        return self.printTree(0)


# root node
class Program(Node):
    def __init__(self, declarations=None, fundefs=None, instructions=None):
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions


# declarations
class Declaration(Node):
    def __init__(self, type=None, inits=None, error=None):
        self.type = type
        self.inits = inits
        self.error = error


class Declarations(Node):
    def __init__(self, declarations=None, declaration=None):
        self.declarations = []
        if declarations is not None:
            self.declarations.extend(declarations.declarations)
        if declaration is not None:
            self.declarations.append(declaration)


class Init(Node):
    def __init__(self, id=None, expression=None):
        self.id = id
        self.expression = expression


class Inits(Node):
    def __init__(self, inits=None, init=None):
        self.inits = []
        if inits is not None:
            self.inits.extend(inits.inits)
        if init is not None:
            self.inits.append(init)


# variable types
class Const(Node):
    def __init__(self, value):
        self.value = value


class Integer(Const):
    def __init__(self, value):
        self.value = value


class Float(Const):
    def __init__(self, value):
        self.value = value


class String(Const):
    def __init__(self, value):
        self.value = value


# instructions
class Instructions(Node):
    def __init__(self, instructions=None, instruction=None):
        self.instructions = []
        if instructions is not None:
            self.instructions = instructions.instructions
        if instruction is not None:
            self.instructions.append(instruction)


class PrintInstr(Node):
    def __init__(self, expression=None):
        self.expression = expression


class LabeledInstr(Node):
    def __init__(self, id, instruction):
        self.id = id
        self.instruction = instruction


class Assignment(Node):
    def __init__(self, id, expression):
        self.id = id
        self.expression = expression


class ChoiceInstr(Node):
    def __init__(self, condition, instruction, else_instruction=None):
        self.condition = condition
        self.instruction = instruction
        self.else_instruction = else_instruction


class WhileInstr(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class RepeatInstr(Node):
    def __init__(self, instructions, condition):
        self.instructions = instructions
        self.condition = condition


class ReturnInstr(Node):
    def __init__(self, expression):
        self.expression = expression


class BreakInstr(Node):
    def __init__(self):
        pass


class ContinueInstr(Node):
    def __init__(self):
        pass


class CompoundInstr(Node):
    def __init__(self, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions


# expressions
class Expression(Node):
    def __init__(self):
        pass


class ConstExpression(Expression):
    def __init__(self, value):
        self.value = value


class IdExpression(Expression):
    def __init__(self, id):
        self.id = id


class BinaryExpression(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class InsideExpression(Expression):
    def __init__(self, expression):
        self.expression = expression


class FunctionExpression(Expression):
    def __init__(self, id, expression):
        self.id = id
        self.expression = expression


class ExpressionList(Node):
    def __init__(self, expr_list=None, expression=None):
        self.expr_list = []
        if expr_list is not None:
            self.expr_list = expr_list.expr_list
        if expression is not None:
            self.expr_list.append(expression)


# fundefs
class Fundefs(Node):
    def __init__(self, fundef=None, fundefs=None):
        self.fundefs = []
        if fundefs is not None:
            self.fundefs = fundefs.fundefs
        if fundef is not None:
            self.fundefs.append(fundef)


class Fundef(Node):
    def __init__(self, type, id, args_list_or_empty, compound_instr):
        self.type = type
        self.id = id
        self.args_list_or_empty = args_list_or_empty
        self.compound_instr = compound_instr


class ArgsList(Node):
    def __init__(self, args_list=None, arg=None):
        self.args_list = []
        if args_list is not None :
            self.args_list = args_list.args_list
        if arg is not None:
            self.args_list.append(arg)


class Arg(Node):
    def __init__(self, type, id):
        self.type = type
        self.id = id