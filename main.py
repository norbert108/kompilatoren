import sys
import ply.yacc as yacc
# import acceptance_test as lol

import TreePrinter
from Cparser import Cparser
from TypeChecker import TypeChecker
from Interpreter import Interpreter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:

        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser)
    text = file.read()

    ast = parser.parse(text, lexer=Cparser.scanner)  # parser
    if ast is None:
        print "Syntax errors."
    else:
        errors = ast.accept2(TypeChecker())                     # lexer
        if errors > 0:
            print "Syntax check completed with {0} errors".format(errors)
        else:
            ast.accept2(Interpreter())                       # interpreter
        #     pass

    # print ast
    # lol.AcceptanceTests()