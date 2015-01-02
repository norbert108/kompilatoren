import ast as AST


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

    @addToClass(AST.Node)
    def printTree(self, level):
        pass

    @addToClass(AST.Program)
    def printTree(self, level):
        tree = ""
        if self.declarations is not None:
            tree += self.declarations.printTree(level)
        if self.fundefs is not None:
            tree += self.fundefs.printTree(level)
        if self.instructions is not None:
            tree += self.instructions.printTree(level)
        return tree

    @addToClass(AST.Declarations)
    def printTree(self, level):
        tree = ""
        for d in self.declarations:
            tree += d.printTree(level)
        return tree

    @addToClass(AST.Declaration)
    def printTree(self, level):
        tree = addLevel(level)
        tree += "DECL\n"
        tree += self.inits.printTree(level+1)
        return tree

    @addToClass(AST.Inits)
    def printTree(self, level):
        tree = ""
        for i in self.inits:
            tree += i.printTree(level)
        return tree

    @addToClass(AST.Init)
    def printTree(self, level):
        tree = addLevel(level)
        tree += "=\n"
        tree += addLevel(level+1)+self.id+"\n"
        tree += self.expression.printTree(level+1)
        return tree

    @addToClass(AST.Fundefs)
    def printTree(self, level):
        tree = ""
        for f in self.fundefs:
            tree += f.printTree(level)
        return tree

    @addToClass(AST.Fundef)
    def printTree(self, level):
        tree = addLevel(level)
        tree += "FUNDEF\n"
        tree += addLevel(level+1)+self.id+"\n"
        tree += addLevel(level+1)+"RET "+self.type+"\n"
        if isinstance(self.args_list_or_empty, AST.ArgsList):
            tree += self.args_list_or_empty.printTree(level+1)

        tree += self.compound_instr.printTree(level+1)
        return tree

    @addToClass(AST.ArgsList)
    def printTree(self, level):
        tree = ""
        for a in self.args_list:
            tree += a.printTree(level)
        return tree

    @addToClass(AST.Arg)
    def printTree(self, level):
        tree = addLevel(level)+"ARG "+self.id+"\n"
        return tree

    @addToClass(AST.Instructions)
    def printTree(self, level):
        tree = ""
        for i in self.instructions:
            tree += i.printTree(level)
        return tree

    @addToClass(AST.PrintInstr)
    def printTree(self, level):
        tree = addLevel(level)+"PRINT"+"\n"
        tree += self.expression.printTree(level+1)
        return tree

    @addToClass(AST.LabeledInstr)
    def printTree(self, level):
        tree = addLevel(level)+self.id+":\n"
        tree += self.instruction.printTree(level+1)
        return tree

    @addToClass(AST.Assignment)
    def printTree(self, level):
        tree = addLevel(level)+"=\n"
        tree += addLevel(level+1)+self.id+"\n"
        tree += self.expression.printTree(level+1)
        return tree

    @addToClass(AST.ChoiceInstr)
    def printTree(self, level):
        tree = addLevel(level)+"IF\n"
        tree += self.condition.printTree(level+1)
        tree += self.instruction.printTree(level+1)
        if self.else_instruction is not None:
            tree += addLevel(level)+"ELSE\n"
            tree += self.instruction.printTree(level+1)
        return tree

    @addToClass(AST.WhileInstr)
    def printTree(self, level):
        tree = addLevel(level)+"WHILE"+"\n"
        tree += self.condition.printTree(level+1)
        tree += self.instruction.printTree(level+1)
        return tree

    @addToClass(AST.RepeatInstr)
    def printTree(self, level):
        tree = addLevel(level)+"REPEAT\n"
        tree += self.instructions.printTree(level+1)
        tree += addLevel(level)+"UNTIL\n"
        tree += self.condition.printTree(level+1)
        return tree

    @addToClass(AST.ReturnInstr)
    def printTree(self, level):
        tree = addLevel(level)+"RETURN\n"
        tree += self.expression.printTree(level+1)
        return tree

    @addToClass(AST.ContinueInstr)
    def printTree(self, level):
        tree = addLevel(level)+"CONTINUE\n"
        return tree

    @addToClass(AST.BreakInstr)
    def printTree(self, level):
        tree = addLevel(level)+"BREAK\n"
        return tree

    @addToClass(AST.CompoundInstr)
    def printTree(self, level):
        tree = self.declarations.printTree(level)
        tree += self.instructions.printTree(level)
        return tree

    @addToClass(AST.ConstExpression)
    def printTree(self, level):
        tree = self.value.printTree(level)
        return tree

    @addToClass(AST.IdExpression)
    def printTree(self, level):
        tree = addLevel(level)+self.id+"\n"
        return tree

    @addToClass(AST.BinaryExpression)
    def printTree(self, level):
        tree = addLevel(level)+self.op+"\n"
        tree += self.left.printTree(level+1)
        tree += self.right.printTree(level+1)
        return tree

    @addToClass(AST.InsideExpression)
    def printTree(self, level):
        tree = self.expression.printTree(level)
        return tree

    @addToClass(AST.FunctionExpression)
    def printTree(self, level):
        tree = addLevel(level)+"FUNCALL\n"
        tree += addLevel(level+1)+self.id+"\n"
        tree += self.expression.printTree(level+1)
        return tree

    @addToClass(AST.ExpressionList)
    def printTree(self, level):
        tree = ""
        for e in self.expr_list:
            tree += e.printTree(level)
        return tree

    @addToClass(AST.Const)
    def printTree(self, level):
        tree = addLevel(level)+self.value+"\n"
        return tree

    @addToClass(AST.Integer)
    def printTree(self, level):
        tree = addLevel(level)+self.value+"\n"
        return tree

    @addToClass(AST.Float)
    def printTree(self, level):
        tree = addLevel(level)+self.value+"\n"
        return tree

    @addToClass(AST.String)
    def printTree(self, level):
        tree = addLevel(level)+self.value+"\n"
        return tree