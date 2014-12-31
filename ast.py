class Node(object):
    def __str__(self):
        return self.printTree()


class Program(Node):
    def __init__(self, declarations=None, fundefs=None, instructions=None):
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions


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


class Variable(Node):
    def __init__(self, value):
        self.value = value
