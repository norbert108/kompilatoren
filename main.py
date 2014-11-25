__author__ = 'norbert'

from plyplus import Grammar

parser = Grammar(r"""

@start: expression ;

?expression: declaration | if | print ;

type: 'int' | 'float' | 'string' ;
identifier: '\w+' ;

parameter_list: '\(' variable (',' variable)* '\)' ;

function: type identifier parameter_list ;
variable: type identifier ;

@declaration: function | variable ;

SPACES: '[ ]+' (%ignore) ;

if: 'if' ;
print: 'print' ;

""")

result = parser.parse("int go(int hhe, float lel)")
print result