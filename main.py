__author__ = 'norbert'

from plyplus import Grammar

parser = Grammar(r"""

@start: expression ;

@expression: function_call | declaration | if | print ;

identifier: '\w+' ;
type: 'int' | 'float' | 'string' ;
value: '\d+' | '"\w+"' ;

parameter_list: '\(' variable? (',' variable)* '\)' ;
arguments_list: '\(' (value)* '\)' ;

assign: identifier '=' value | variable '=' value;

function_body: '\{' (expression)* '\}' ;
function_call: identifier arguments_list ';' expression? ;
function_def: type identifier parameter_list function_body ;

variable: type identifier ;

declaration: (function_def | (type (identifier | assign) (',' (identifier | assign))* ';')) expression? ;

SPACES: '[ ]+' (%ignore) ;
WS: '[ \t\n]+' (%ignore) (%newline);

if: 'if' ;
print: 'print' ;

""")

result = parser.parse("""
int urmom = 0, iii;
int twojastara(int zapierdala){}
tytytyt();
""")
print result