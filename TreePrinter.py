import ast


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


def addLevel(level):
    r = ""
    for i in xrange(level):
        r += "| "
    return r


class TreePrinter:

    @addToClass(ast.Node)
    def printTree(self, level):
        pass

    @addToClass(ast.Program)
    def printTree(self, level):
        tree = ""
        if self.declarations is not None:
            tree += self.declarations.printTree(level)
        if self.fundefs is not None:
            tree += self.fundefs.printTree(level)
        if self.instructions is not None:
            tree += self.instructions.printTree(level)
        return tree

    @addToClass(ast.Declarations)
    def printTree(self, level):
        tree = ""
        for d in self.declarations:
            tree += d.printTree(level)
        return tree

    @addToClass(ast.Declaration)
    def printTree(self, level):
        tree = addLevel(level)
        tree += "DECL\n"
        tree += self.inits.printTree(level+1)
        return tree

    @addToClass(ast.Inits)
    def printTree(self, level):
        tree = ""
        for i in self.inits:
            tree += i.printTree(level)
        return tree

    @addToClass(ast.Init)
    def printTree(self, level):
        tree = addLevel(level)
        tree += "=\n"
        tree += addLevel(level+1)+self.id+"\n"
        tree += self.expression.printTree(level+1)
        return tree

    @addToClass(ast.Fundefs)
    def printTree(self, level):
        tree = ""
        for f in self.fundefs:
            tree += f.printTree(level)
        return tree

    @addToClass(ast.Fundef)
    def printTree(self, level):
        tree = addLevel(level)
        tree += "FUNDEF\n"
        tree += addLevel(level+1)+self.id+"\n"
        tree += addLevel(level+1)+"RET "+self.type+"\n"
        if isinstance(self.args_list_or_empty, ast.ArgsList):
            tree += self.args_list_or_empty.printTree(level+1)

        tree += self.compound_instr.printTree(level+1)
        return tree

    @addToClass(ast.ArgsList)
    def printTree(self, level):
        tree = ""
        for a in self.args_list:
            tree += a.printTree(level)
        return tree

    @addToClass(ast.Arg)
    def printTree(self, level):
        tree = addLevel(level)+"ARG "+self.id+"\n"
        return tree

    @addToClass(ast.Instructions)
    def printTree(self, level):
        tree = ""
        for i in self.instructions:
            tree += i.printTree(level)
        return tree

    @addToClass(ast.PrintInstr)
    def printTree(self, level):
        tree = addLevel(level)+"PRINT"+"\n"
        tree += self.expression.printTree(level+1)
        return tree

    @addToClass(ast.LabeledInstr)
    def printTree(self, level):
        tree = addLevel(level)+self.id+":\n"
        tree += self.instruction.printTree(level+1)
        return tree

    @addToClass(ast.Assignment)
    def printTree(self, level):
        tree = addLevel(level)+"=\n"
        tree += addLevel(level+1)+self.id+"\n"
        tree += self.expression.printTree(level+1)
        return tree

    @addToClass(ast.ChoiceInstr)
    def printTree(self, level):
        tree = addLevel(level)+"IF\n"
        tree += self.condition.printTree(level+1)
        tree += self.instruction.printTree(level+1)
        if self.else_instruction is not None:
            tree += addLevel(level)+"ELSE\n"
            tree += self.instruction.printTree(level+1)
        return tree

    @addToClass(ast.WhileInstr)
    def printTree(self, level):
        tree = addLevel(level)+"WHILE"+"\n"
        tree += self.condition.printTree(level+1)
        tree += self.instruction.printTree(level+1)
        return tree

    @addToClass(ast.RepeatInstr)
    def printTree(self, level):
        tree = addLevel(level)+"REPEAT\n"
        tree += self.instructions.printTree(level+1)
        tree += addLevel(level)+"UNTIL\n"
        tree += self.condition.printTree(level+1)
        return tree

    @addToClass(ast.ReturnInstr)
    def printTree(self, level):
        tree = addLevel(level)+"RETURN\n"
        tree += self.expression.printTree(level+1)
        return tree

    @addToClass(ast.ContinueInstr)
    def printTree(self, level):
        tree = addLevel(level)+"CONTINUE\n"
        return tree

    @addToClass(ast.BreakInstr)
    def printTree(self, level):
        tree = addLevel(level)+"BREAK\n"
        return tree

    @addToClass(ast.CompoundInstr)
    def printTree(self, level):
        tree = self.declarations.printTree(level)
        tree += self.instructions.printTree(level)
        return tree

    @addToClass(ast.ConstExpression)
    def printTree(self, level):
        tree = self.value.printTree(level)
        return tree

    @addToClass(ast.IdExpression)
    def printTree(self, level):
        tree = addLevel(level)+self.id+"\n"
        return tree

    @addToClass(ast.BinaryExpression)
    def printTree(self, level):
        tree = addLevel(level)+self.op+"\n"
        tree += self.left.printTree(level+1)
        tree += self.right.printTree(level+1)
        return tree

    @addToClass(ast.InsideExpression)
    def printTree(self, level):
        tree = self.expression.printTree(level)
        return tree

    @addToClass(ast.FunctionExpression)
    def printTree(self, level):
        tree = addLevel(level)+"FUNCALL\n"
        tree += addLevel(level+1)+self.id+"\n"
        tree += self.expression.printTree(level+1)
        return tree

    @addToClass(ast.ExpressionList)
    def printTree(self, level):
        tree = ""
        for e in self.expr_list:
            tree += e.printTree(level)
        return tree

    @addToClass(ast.Const)
    def printTree(self, level):
        tree = addLevel(level)+self.value+"\n"
        return tree

    @addToClass(ast.Integer)
    def printTree(self, level):
        tree = addLevel(level)+self.value+"\n"
        return tree

    @addToClass(ast.Float)
    def printTree(self, level):
        tree = addLevel(level)+self.value+"\n"
        return tree

    @addToClass(ast.String)
    def printTree(self, level):
        tree = addLevel(level)+self.value+"\n"
        return tree